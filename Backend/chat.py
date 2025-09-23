from gpt4all import GPT4All
from pathlib import Path
from os import getcwd
import json
import re

from db import recommend_similar_supplements  

model_path = Path(getcwd()) / "models" / "llama-2-7b-chat.Q4_K_S.gguf"
llm = GPT4All(str(model_path))

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


def ask_llm(query: str) -> dict:
    prompt = f"""
    You are a medical symptom extractor.
    Input: "{query}"
    Task: Return ONLY a JSON object with all symptoms mentioned. 
    Example: {{"symptoms": ["headache", "fever"]}}
    Do not add explanations or text.
    """

    with llm.chat_session():
        answer = llm.generate(prompt, max_tokens=200, temp=0.5)

    return extract_json(answer)

def ans_llm(query: str, ans: str, history: list[str] | None = None) -> str:
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
    with llm.chat_session():
        answer = llm.generate(prompt, max_tokens=200, temp=0.5).strip()

    return answer


def get_answer(query: str, history: list[str] | None = None) -> str:
    symptoms_json = ask_llm(query)
    symptoms = symptoms_json.get("symptoms", [])
    if not symptoms:
        return "Sorry, I couldn't identify any symptoms in your query."

    db_results = recommend_similar_supplements(" ".join(symptoms))
    if not db_results:
        return "Sorry, I couldn't find any supplements related to your symptoms."

    ans = ans_llm(query, db_results, history)
    return ans

if __name__ == "__main__":
    print("LLaMA 2–7B loaded successfully")
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
        




      