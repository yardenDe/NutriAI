from google import genai
from dotenv import load_dotenv
import os
import json
import re
from db import recommend_similar_supplements  

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=api_key)

def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text.strip(), re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"Parse error: {e}\nRaw json: {json_str}")
            return {"symptoms": []}
    else:
        print(f"No JSON found in: {text}")
        return {"symptoms": []}

def ask_gemini(query: str) -> dict:
    chat = client.chats.create(model="gemini-2.0-flash")
    prompt = f"""
    You are a medical symptom extractor.
    Input: "{query}"
    Task: Return ONLY a JSON object with all symptoms mentioned.
    Example: {{"symptoms": ["headache", "fever"]}}
    Do not add explanations or text.
    """
    response = chat.send_message(prompt)
    return extract_json(response.text)

def ans_gemini(query: str, ans: str, history: list[str] | None = None) -> str:
    chat = client.chats.create(model="gemini-2.0-flash")
    history_text = ""
    if history:
        history_text = "\nConversation so far:\n"
        for h in history:
            history_text += f"{h}\n"
    prompt = f"""
    {history_text}
    User: {query}
    System: We searched our supplement database and found the following relevant results: {ans}
    Task:
    - Write a short, user-friendly answer in simple language.
    - Summarize the supplements in a clear way.
    - Do not invent information that is not in the results.
    Assistant:
    """
    response = chat.send_message(prompt)
    return response.text.strip()

def get_answer(query: str, history: list[str] | None = None) -> str:
    symptoms_json = ask_gemini(query)
    symptoms = symptoms_json.get("symptoms", [])
    if not symptoms:
        return "Sorry, I couldn't identify any symptoms in your query."
    db_results = recommend_similar_supplements(" ".join(symptoms))
    if not db_results:
        return "Sorry, I couldn't find any supplements related to your symptoms."
    ans = ans_gemini(query, db_results, history)
    return ans

if __name__ == "__main__":
    print("Gemini Client loaded successfully")
    print("Type 'x' to exit.")
    history = []
    while True:
        query = input("\nYou: ")
        if query.lower() == "x":
            break
        print("Current history:", history)
        result = get_answer(query, history)
        print("Assistant:", result)
        history.append(f"User: {query}")
        history.append(f"Assistant: {result}")
