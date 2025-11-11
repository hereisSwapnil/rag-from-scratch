# provider/openai_provider.py

import os
from provider.base import BaseProvider
import openai
from openai import AuthenticationError, RateLimitError, APIConnectionError

class OpenAIProvider(BaseProvider):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)

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
                                content = chunk.choices[0].delta.content
                                if content:
                                    yield content
                    except Exception as e:
                        raise Exception(f"Error in OpenAI streaming: {str(e)}")
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
                raise RuntimeError("⚠️ Empty response from OpenAI API")
            
            if not response.choices[0].message:
                raise RuntimeError("⚠️ No message in OpenAI response")
            
            content = response.choices[0].message.content
            
            if not content or not content.strip():
                return "I apologize, but I couldn't generate a response."
            
            return content
            
        except AuthenticationError:
            raise ValueError("❌ Invalid API Key. Re-generate it here: https://platform.openai.com/account/api-keys")

        except RateLimitError:
            raise RuntimeError("⏳ Rate limit exceeded. Try again later or upgrade your plan.")

        except APIConnectionError:
            raise RuntimeError("🌐 Network issue. Check your internet connection.")

        except Exception as e:
            raise RuntimeError(f"⚠️ Unexpected OpenAI Error: {e}")
