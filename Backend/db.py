import psycopg2
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer




load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_cvs_path(filename: str = "products_with_purpose.csv") -> Path:
    base_path = Path(__file__).resolve().parent.parent
    CSV_PATH = base_path / "DataBase" / filename
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"File not found in path: {CSV_PATH}")
    return CSV_PATH

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

# SUPPLEMENTS
def insert_supplements_from_csv():
    CSV_PATH = get_cvs_path()
    
    data = pd.read_csv(CSV_PATH)
    sample = data.sample(n = 250).reset_index(drop=True)

    print(f"Read {len(data)} rows from CSV file successfully")
    
    conn = connect_to_db()
    cur = conn.cursor()

    for idx, row in sample.iterrows():
        name = row["name"]
        desc = row["description"]
        embedded = to_embedded(desc)

        ##DEBUG PRINT 
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
    print (f"embedded_goal = {embedded_goal}")

    try:
        cur.execute(
            "SELECT * FROM find_supplements(%s, %s);",
            (embedded_goal, top_n)
        )
        results = cur.fetchall()

        print (results)

        for idx, rec in enumerate(results, start=1):
            print(f"Result {idx}: {rec[1]} (similarity: {rec[3]:.4f})")

        return results
    except Exception as e:
        print(f" Error during recommendation: {e}")
        return []
    finally:
        disconnect_from_db(conn, cur)

# USERS

def add_user(username: str, password: str):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT add_user(%s, %s);", (username, password))
        conn.commit()
        result = cur.fetchone()[0]
        return result
    finally:
        disconnect_from_db(conn, cur)


def authenticate_user(username: str, password: str):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT authenticate(%s, %s);", (username, password))
        result = cur.fetchone()[0]
        return result
    finally:
        disconnect_from_db(conn, cur)


# CHAT HISTORY

def add_chat_message(user_id: int, role: str, content: str):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT add_chat_message(%s, %s, %s);",
                    (user_id, role, content))
        conn.commit()
    finally:
        disconnect_from_db(conn, cur)


def get_last_messages(user_id: int, limit: int = 5):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_last_messages(%s, %s);", (user_id, limit))
        result = cur.fetchall()

        return result
    finally:
        disconnect_from_db(conn, cur)


# CHAT SUMMARY

def get_chat_summary(user_id: int):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT get_chat_summary(%s);", (user_id,))
        result = cur.fetchone()[0]
        return result
    finally:
        disconnect_from_db(conn, cur)


def update_chat_summary(user_id: int, summary: str):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT update_chat_summary(%s, %s);",
                    (user_id, summary))
        conn.commit()
    finally:
        disconnect_from_db(conn, cur)


def get_last_summary_time(user_id: int):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT get_summary_time(%s);", (user_id,))
        result = cur.fetchone()[0]
        return result
    finally:
        disconnect_from_db(conn, cur)


def count_new_messages(user_id: int, last_summary_time):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT count_new_messages(%s, %s);",
            (user_id, last_summary_time)
        )
        result = cur.fetchone()[0]
        return result
    finally:
        disconnect_from_db(conn, cur)


# LOGIC: update summary when needed ---------------------

def update_summary_if_needed(user_id: int):
    from llm import summarize_conversation

    # 1) get last summary timestamp
    last_summary_time = get_last_summary_time(user_id)

    # 2) CASE 1: user has NO summary yet
    if last_summary_time is None:
        # count ALL messages
        new_msgs = get_last_messages(user_id, 9999)

        # no messages → nothing to do
        if not new_msgs or len(new_msgs) == 0:
            return  

        # if less than 10 messages → wait
        if len(new_msgs) < 10:
            return  

        # summarize ALL messages
        parts = [f"{role}: {content}" for role, content, ts in reversed(new_msgs)]
        to_summarize = "\n".join(parts)

        new_summary = summarize_conversation(to_summarize)
        update_chat_summary(user_id, new_summary)
        return


    # 3) CASE 2: user HAS previous summary
    new_count = count_new_messages(user_id, last_summary_time)

    print(f"New messages since last summary: {new_count}")

    if new_count < 10:
        return  # nothing to summarize yet

    # fetch only new messages
    new_msgs = get_last_messages(user_id, new_count)

    old_summary = get_chat_summary(user_id)

    parts = []

    if old_summary:
        parts.append(f"Previous summary:\n{old_summary}\n")

    for role, content, created_at in reversed(new_msgs):
        parts.append(f"{role}: {content}")

    to_summarize = "\n".join(parts)

    new_summary = summarize_conversation(to_summarize)
    update_chat_summary(user_id, new_summary)
