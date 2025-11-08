from fastapi import FastAPI, Query
from pydantic import BaseModel
from db import recommend_similar_supplements, connect_to_db, disconnect_from_db
from llm import get_answer

def setup_routes(app: FastAPI):
    
    sessions = {}

    class ChatRequest(BaseModel):
        session_id: str
        text: str

    class ChatResponse(BaseModel):
        answer: str

    def process_message(session_id: str, user_text: str) -> str:
        if session_id not in sessions:
            sessions[session_id] = []

        sessions[session_id].append({"role": "user", "content": user_text})
        history = [f"{m['role'].capitalize()}: {m['content']}" for m in sessions[session_id]]
        answer = get_answer(user_text, history)
        sessions[session_id].append({"role": "assistant", "content": answer})

        return answer

    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest):
        ans = process_message(req.session_id, req.text)
        return ChatResponse(answer=ans)

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
