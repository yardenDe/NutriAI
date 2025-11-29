from fastapi import FastAPI, Query, Depends, HTTPException
from pydantic import BaseModel
from jwt_handler import verify_token
from db import (
    recommend_similar_supplements,
    add_chat_message,
    get_last_messages,
    get_chat_summary,
    update_chat_summary,
    update_summary_if_needed,
    connect_to_db, disconnect_from_db
)
from llm import get_answer


def setup_routes(app: FastAPI):

    class ChatRequest(BaseModel):
        text: str

    class ChatResponse(BaseModel):
        answer: str

    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest, payload: dict = Depends(verify_token)):
        user_id = payload["user_id"]

        summary = get_chat_summary(user_id)
        print (summary)

        history_list = get_last_messages(user_id, 5)

        history = []
        if summary:
            history.append(f"Summary: {summary}")

        for h in reversed(history_list):  # oldest first
            role, content, created_at = h
            history.append(f"{role.capitalize()}: {content}")

        add_chat_message(user_id, "user", req.text)
        answer = get_answer(req.text, history)
        add_chat_message(user_id, "assistant", answer)
        update_summary_if_needed(user_id)


        return ChatResponse(answer=answer)


    @app.get("/recommendations")
    async def recommendations(symptoms: list[str] = Query(None)):
        if not symptoms:
            print ("no symptoms")
            return {"error": "No symptoms provided"}
        all_symptoms = " ".join(symptoms)
        print(all_symptoms)
        recs = recommend_similar_supplements(all_symptoms)
        print (recs)
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
            cur.execute(
                "SELECT name, description FROM supplements WHERE name = %s;",
                (name,),
            )
            result = cur.fetchone()
            if result:
                return {"name": result[0], "description": result[1]}
            return {"error": "Supplement not found"}
        finally:
            disconnect_from_db(conn, cur)
