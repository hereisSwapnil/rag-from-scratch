# ingest/chunker.py

def split(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split the text into chunks of the given size, with the given overlap."""
    
    text = text.strip().replace("\n\n", "\n")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
