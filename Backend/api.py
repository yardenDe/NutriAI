from fastapi import FastAPI, Query
from db import recommend_similar_supplements, connect_to_db, disconnect_from_db

def setup_routes(app: FastAPI):
    
    @app.get("/recommendations")
    async def recommendations(symptoms: list[str] = Query(None)):
        if not symptoms:
            return {"error": "No symptoms provided"}
        all_symptoms = " ".join(symptoms)
        recs = recommend_similar_supplements(all_symptoms)
        return {"recommendations": recs}

    @app.get("/supplements")
    async def list_supplements():
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
