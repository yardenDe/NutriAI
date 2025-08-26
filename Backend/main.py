from fastapi import FastAPI, Body
import psycopg2
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Load environment variables (e.g. API keys) from .env
load_dotenv()

# Initialize OpenAI client using API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def to_embedded(desc: str):
    """
    Generate an embedding vector for a given text description
    using OpenAI's embeddings API.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",  # 1536-dim embeddings model
        input=desc
    )
    return response.data[0].embedding

# 2. Load the CSV file with supplements data
csv_path = r"C:\Users\User\Personal_Projects\NutriAI\SQL\supplements_tamp.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found in path: {csv_path}")

# Load CSV into a DataFrame
data = pd.read_csv(csv_path)
print(f"Read {len(data)} rows from CSV file successfully")


# 3. Connect to Supabase (Postgres database)
conn = psycopg2.connect(
    dbname="postgres",                   
    user="postgres",                    
    password= os.getenv("SUPABASE_PASSWORS") ,   
    host="db.ailnvqajkzfxdeipdvdy.supabase.co",     
    port="5432",
    sslmode="require"
)
cur = conn.cursor()

# 4. Insert data row-by-row into the database
for idx, row in data.iterrows():
    name = row["name"]
    desc = row["description"] 

    # Generate embedding for the description
    embedded = to_embedded(desc)

    # Insert into DB using your custom SQL function add_supplements
    cur.execute(
        """SELECT add_supplements(%s, %s, %s);""",
        (name, desc, embedded)
    )
    print(f"Inserted {name} into the database.")

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()

print("All supplements inserted with embeddings!")

# 5. FastAPI application (demo endpoints)
app = FastAPI()

# Temporary in-memory database for demo
DB = []

class Supplement:
    """
    A simple Supplement class to simulate supplement objects
    stored in memory for the FastAPI demo endpoints.
    """
    def __init__(self, slug: str, name: str, goals: list[str] = None):
        self.slug = slug
        self.name = name
        self.goals = goals if goals is not None else []

    def to_dict(self):
        """Convert the Supplement object into a serializable dict"""
        return {
            "slug": self.slug,
            "name": self.name,
            "goals": self.goals,
        }

@app.get("/")
async def root():
    """Root endpoint that returns basic info"""
    return {"ok": True, "count": len(DB)}

@app.get("/supplements")
async def list_supplements():
    """Return a list of all supplements (from in-memory DB)"""
    return [sup.to_dict() for sup in DB]

@app.post("/supplements")
async def add_supplement(data: dict = Body(...)):
    """
    Add a new supplement to the in-memory DB.
    Requires: slug, name, goals (optional).
    """
    slug = data.get("slug")
    name = data.get("name", "")
    goals = data.get("goals", [])
    if not slug:
        return {"error": "slug is required"}
    for sup in DB:
        if sup.slug == slug:
            return {"error": "slug already exists"}
    supplement = Supplement(slug, name, goals)
    DB.append(supplement)
    return supplement.to_dict()

@app.get("/supplements/{slug}")
async def get_supplement(slug: str):
    """Retrieve a supplement by its slug"""
    for sup in DB:
        if sup.slug == slug:
            return sup.to_dict()
    return {"error": "not found"}

# Demo data 
DB.append(Supplement("vitamin-c", "Vitamin C", ["immune", "antioxidant"]))
DB.append(Supplement("omega-3", "Omega 3", ["heart", "brain"]))
DB.append(Supplement("magnesium", "Magnesium", ["muscle", "sleep"]))

