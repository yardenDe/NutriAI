
class LLMManager:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> str:
        chat = self.client.chats.create(model=self.model)
        response = chat.send_message(prompt)
        return response.text.strip()

