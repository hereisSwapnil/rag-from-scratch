# main.py

from provider.ollama_provider import OllamaProvider
from vectorstore.chroma_db import semantic_search, get_collection, check_and_index_files
from memory.chat_memory import ChatMemory
from prompt.prompt import SYSTEM_PROMPT, USER_PROMPT

def build_prompt(context_chunks, query):
    if context_chunks:
        retrieved_context = "\n\n".join(context_chunks)
    else:
        retrieved_context = "No relevant context found in the documents."
    
    user_message = USER_PROMPT.format(
        retrieved_context=retrieved_context,
        user_query=query
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

def main():
    # Check and index files before starting
    print("🔍 Checking if all files in data folder are indexed...")
    check_and_index_files("data")
    print()
    
    print("📚 RAG Chatbot Ready. Type 'exit' to quit.")

    llm = OllamaProvider(model="gpt-oss:120b-cloud")
    memory = ChatMemory()
    collection = get_collection()

    while True:
        user_query = input("\nYou: ")

        if user_query.lower() in {"exit", "quit"}:
            print("Goodbye 👋")
            break

        try:
            results = semantic_search(collection, user_query, n_results=4)
            context_chunks = results["documents"][0] if results["documents"] else []

            messages = build_prompt(context_chunks, user_query)

            messages = messages + memory.get()

            response = llm.chat(messages)
            
            if not response or not response.strip():
                response = "I apologize, but I couldn't generate a response. Please try rephrasing your question."

            memory.add("user", user_query)
            memory.add("assistant", response)

            print(f"\nAssistant: {response}")
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            print(f"\nAssistant: {error_msg}")
            print(f"Debug: {type(e).__name__}")

if __name__ == "__main__":
    main()
