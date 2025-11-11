# provider/groq_provider.py

from groq import Groq
from provider.base import BaseProvider
import os


class GroqProvider(BaseProvider):
    def __init__(self, model="llama3.1:8b", api_key=None):
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        if api_key is None:
            raise ValueError("GROQ_API_KEY is not set")
        self.model = model
        self.client = Groq(api_key=api_key)

    def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 8192, stream: bool = False):
        try:
            if stream:
                def stream_generator():
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            stream=True,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            timeout=120
                        )
                        for chunk in response:
                            if chunk.choices and chunk.choices[0].delta:
                                delta = chunk.choices[0].delta
                                if delta and delta.content:
                                    yield delta.content
                    except Exception as e:
                        raise Exception(f"Error in Groq streaming: {str(e)}")
                return stream_generator()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=120
            )
            
            if not response or not response.choices:
                raise RuntimeError("⚠️ Empty response from Groq API")
            
            if not response.choices[0].message:
                raise RuntimeError("⚠️ No message in Groq response")
            
            content = response.choices[0].message.content
            
            if not content or not content.strip():
                return "I apologize, but I couldn't generate a response."
            
            return content
            
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
