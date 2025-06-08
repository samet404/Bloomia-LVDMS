import logging

from google import genai


class GeminiClientPool:
    def __init__(self, api_keys: list[str]):
        self.api_keys = api_keys
        self.current_index = 0
        self.clients = []

        for api_key in api_keys:
            client = genai.Client(api_key=api_key)
            self.getResponse(model="gemini-2.0-flash", contents="")

            self.clients.append(genai.Client(api_key=api_key))

    def getResponseStream(self, model: str, contents: str):
        try:
            client = self.clients[self.current_index]

            stream = client.models.generate_content_stream(
                model=model,
                contents=contents
            )
            self.current_index += 1
            return stream
        except:
            self.current_index += 1
            logging.error(f"Error in getResponseStream: {model}, {contents}")

    def getResponse(self, model: str, contents: str):
        try:
            client = self.clients[self.current_index]

            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            self.current_index += 1
            return response
        except:
            self.current_index += 1
            logging.error(f"Error in getResponse: {model}, {contents}")