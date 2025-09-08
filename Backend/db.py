import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

CSV_PATH = r"C:\Users\User\Personal_Projects\NutriAI\SQL\products_with_purpose.csv"
model = SentenceTransformer("all-MiniLM-L6-v2")


def to_embedded(desc: str):
    emb_list = model.encode(desc).tolist()
    emb_str  = "[" + ",".join(str(x) for x in emb_list) + "]"
    return emb_str

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname ="postgres",                   
            user ="postgres",                    
            password = os.getenv("SUPABASE_PASSWORD"),
            host = "db.ailnvqajkzfxdeipdvdy.supabase.co",
            port = "5432",
            sslmode = "require"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def disconnect_from_db(conn, cur):
    try:
        if cur: cur.close()
        if conn: conn.close()
    except Exception as e:
        print(f"Failed to close connection: {e}")
        raise

def insert_supplements_from_csv():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"File not found in path: {CSV_PATH}")
    
    data = pd.read_csv(CSV_PATH)
    sample = data.sample(n = 250).reset_index(drop=True)

    print(f"Read {len(data)} rows from CSV file successfully")
    
    conn = connect_to_db()
    cur = conn.cursor()

    for idx, row in sample.iterrows():
        name = row["name"]
        desc = row["description"]
        embedded = to_embedded(desc)

        print(f"Inserting {name}...")
        print(f"Description: {desc[:60]}...")
        print(f"Embedding length: {len(embedded)}")
        cur.execute(
            """SELECT add_supplements(%s, %s, %s);""",
            (name, desc, embedded)
        )
        print(f"Inserted {name} into the database.")
    
    conn.commit()
    disconnect_from_db(conn, cur)
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

        for idx, rec in enumerate(results, start=1):
            print(f"Result {idx}: {rec[1]} (similarity: {rec[3]:.4f})")

        return results
    except Exception as e:
        print(f" Error during recommendation: {e}")
        return []
    finally:
        disconnect_from_db(conn, cur)

