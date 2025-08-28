from fastapi import FastAPI, Query
import psycopg2
import pandas as pd
import os
import random
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_DIM = 1536

def to_embedded(desc: str):
    emb =  [random.uniform(-1.0, 1.0) for _ in range(EMBEDDING_DIM)]
    return "[" + ",".join(map(str, emb)) + "]"


csv_path = r"C:\Users\User\Personal_Projects\NutriAI\SQL\supplements_tamp.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found in path: {csv_path}")

# Load CSV into a DataFrame
data = pd.read_csv(csv_path)
print(f"Read {len(data)} rows from CSV file successfully")

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",                   
            user="postgres",                    
            password=os.getenv("SUPABASE_PASSWORD"),
            host="db.ailnvqajkzfxdeipdvdy.supabase.co",
            port="5432",
            sslmode="require"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
    
def disconnect_from_db(conn, cur):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()        
    except Exception as e:
        print(f"Failed to close connection: {e}")
        raise


conn = connect_to_db()
cur = conn.cursor()

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
disconnect_from_db( conn, cur)
print("All supplements inserted with embeddings!")


def recommend_similar_supplements(goal: str, top_n: int = 5):
    conn = connect_to_db()
    cur = conn.cursor()
    embedded_goal = to_embedded(goal)
    try:
        cur.execute(
           "SELECT * FROM find_supplements(%s, %s);",
            (embedded_goal, top_n)
        )
        results = cur.fetchall()
        return results
    except Exception as e:
        print(f"Error during recommendation: {e}")
        return []
    finally:
        disconnect_from_db(conn, cur)


# FastAPI app
app = FastAPI()

@app.get("/recommendations")
async def recommendations(symptoms: list[str] = Query(None)):
    """Get supplement recommendations based on user symptoms/goals"""
    if not symptoms:
        return {"error": "No symptoms provided"}
    
    all_symptoms = " ".join(symptoms)
    recs = recommend_similar_supplements(all_symptoms)
    return {"recommendations": recs}

@app.get("/supplements")
async def list_supplements():
    """Return all supplements in the database"""
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name, description FROM supplements;")
        results = cur.fetchall()
        return [{"name": r[0], "description": r[1]} for r in results]
    finally:
        disconnect_from_db(conn, cur)

@app.get("/supplements/{name}")
async def get_supplement(name: str):
    """Retrieve a supplement by name"""
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name, description FROM supplements WHERE name = %s;", (name,))
        result = cur.fetchone()
        if result:
            return {"name": result[0], "description": result[1]}
        return {"error": "Supplement not found"}
    finally:
        disconnect_from_db(conn, cur)