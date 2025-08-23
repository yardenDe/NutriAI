from fastapi import FastAPI, Body
import psycopg2
from openai import OpenAI

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


