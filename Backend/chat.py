from gpt4all import GPT4All
from pathlib import Path
from os import getcwd
import json

model_path = Path(getcwd()) / "models" / "llama-2-7b-chat.Q4_K_S.gguf"
llm = GPT4All(str(model_path))

print("running -  LLaMA 2–7B! - model loaded successfully")

def get_symptoms(query: str):
    if not query or query.lower() == 'x':
        return None

    system_prompt = """
    You are an AI assistant.
    Extract all the symptoms from the user's query.
    Return each symptom on a separate line, without numbering or extra text.
    Example output:
    headache
    fever
    nausea
    """

    full_prompt = f"{system_prompt}\n\nUser: {query}\nBot:"

    with llm.chat_session():
        answer = llm.generate(full_prompt, max_tokens=200, temp=0.5)

    try:
        print("in try to parse answer answer:", answer)
        symptoms = json.loads(answer)
        print("Bot (parsed):", symptoms)
        return symptoms
    except json.JSONDecodeError:
        print(" Could not parse answer:", answer)
        return []
    
def get_answer():
    with llm.chat_session():
        while True:
            if query.lower() == 'x':
                break
            answer = llm.generate(query, max_tokens=200, temp=0.5)
            print("Bot:", answer)
        return answer
    
if __name__ == "__main__":
    print("Type 'x' to exit.")
    while True:
        query = input("You: ")
        if query.lower() == 'x':
            break
        print("before get_symptoms")
        s = (get_symptoms(query))
        print("after get_symptoms")
        print("Extracted symptoms:", s)
    