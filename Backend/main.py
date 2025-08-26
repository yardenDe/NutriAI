from fastapi import FastAPI, Body
import psycopg2
from openai import OpenAI
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="",
    input = 
)

# Temporary CSV path for demonstration purposes
cvs_path = "C:\\Users\\User\\Personal_Projects\\NutriAI\\SQL\\supplements_tamp.csv"
data = pd.read_csv(cvs_path)

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found in path: {csv_path}")

data = pd.read_csv(csv_path)
print( " Read {len(data)} from CSV file successfully")

# Connect to Supabase PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",                   
    user="postgres",                    
    password="zurqub-mecbof-7Dexxi",   
    host="db.ailnvqajkzfxdeipdvdy.supabase.co",           
    port="5432",
    sslmode="require"
)
cur = conn.cursor()

for idx, row in data.iterrows():
    name = row["name"]
    desc = row["description"]
    cur.execute(""" SELECT add_supplements(%s, %s, %s); """, (name, desc, None))   
    print(f"Inserted {name} into the database.")

conn.commit()
cur.close()
conn.close()


app = FastAPI()

DB = []

class Supplement:
    def __init__(self, slug: str, name: str, goals: list[str] = None):
        self.slug = slug
        self.name = name
        self.goals = goals if goals is not None else []

    def to_dict(self):
        return {
            "slug": self.slug,
            "name": self.name,
            "goals": self.goals,
        }

@app.get("/")
async def root():
    return {"ok": True, "count": len(DB)}

@app.get("/supplements")
async def list_supplements():
    return [sup.to_dict() for sup in DB]

@app.post("/supplements")
async def add_supplement(data: dict = Body(...)):
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
    for sup in DB:
        if sup.slug == slug:
            return sup.to_dict()
    return {"error": "not found"}


DB.append(Supplement("vitamin-c", "Vitamin C", ["immune", "antioxidant"]))
DB.append(Supplement("omega-3", "Omega 3", ["heart", "brain"]))
DB.append(Supplement("magnesium", "Magnesium", ["muscle", "sleep"]))


