# provider/ollama_provider.py

import requests
import json
from provider.base import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self, model="llama3"):
        self.model = model

    def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 8192, stream: bool = False):
        if stream:
            def stream_generator():
                res = requests.post(
                    "http://localhost:11434/api/chat",
                    json={"model": self.model, "messages": messages, "stream": True, "temperature": temperature, "max_tokens": max_tokens},
                    stream=True,
                    timeout=120
                )
                for line in res.iter_lines():
                    if not line:
                        continue
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
            return stream_generator()

        try:
            res = requests.post(
                "http://localhost:11434/api/chat",
                json={"model": self.model, "messages": messages, "stream": False, "temperature": temperature, "max_tokens": max_tokens},
                timeout=120
            )
            res.raise_for_status()
            data = res.json()
            
            if "message" in data:
                if isinstance(data["message"], dict) and "content" in data["message"]:
                    content = data["message"]["content"]
                    return content if content else "I apologize, but I couldn't generate a response."
                elif isinstance(data["message"], str):
                    return data["message"]
            
            if "response" in data:
                return data["response"] if data["response"] else "I apologize, but I couldn't generate a response."
            
            print(f"Warning: Unexpected response structure: {data}")
            return "I apologize, but I encountered an issue generating a response."
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Ollama API: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Ollama API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling Ollama API: {str(e)}")
