# vectorstore/chroma_db.py

import chromadb
from chromadb.utils import embedding_functions
import os
from ingest.chunker import split
from ingest.loader import load

# Private methods
def _process_document(file_path):
    """Process a document and return chunks, metadata, and IDs."""
    try:
        text = load(file_path)
        chunks = split(text)

        file_name = os.path.basename(file_path)
        metadata = [
            {"source": file_name, "chunk_index": i} for i in range(len(chunks))
        ]
        ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]
        return ids, chunks, metadata
    except Exception as e:
        print(f"Error processing document {file_path}: {e}")
        return [], [], []

def _add_to_collection(collection, ids, chunks, metadata):
    """Add chunks to the collection."""
    if not chunks:
        print("No chunks to add to the collection.")
        return
    
    batch_size = 100

    for i in range(0, len(chunks), batch_size):
        end_idx = min(i + batch_size, len(chunks))
        collection.add(
            ids=ids[i:end_idx],
            documents=chunks[i:end_idx],
            metadatas=metadata[i:end_idx]
        )

# Public methods
def get_collection(path="storage/chroma_db", name="documents_collection"):
    """Get or create a collection."""
    client = chromadb.PersistentClient(path=path)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(name=name, embedding_function=embedding_fn)

def process_and_add_to_collection(collection, folder_path: str):
    """Process and add files to the collection."""
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        file_path = os.path.join(folder_path, file)
        ids, chunks, metadata = _process_document(file_path)
        _add_to_collection(collection, ids, chunks, metadata)

def semantic_search(collection, query: str, n_results: int = 4):
    """Perform semantic search on the collection."""
    results = collection.query(query_texts=[query], n_results=n_results)
    return results

def get_indexed_files(collection):
    """Get a set of all file names that are currently indexed in the collection."""
    try:
        all_data = collection.get()
        
        if not all_data or not all_data.get('metadatas'):
            return set()
        
        indexed_files = set()
        for metadata in all_data['metadatas']:
            if metadata and 'source' in metadata:
                indexed_files.add(metadata['source'])
        
        return indexed_files
    except Exception as e:
        print(f"Error getting indexed files: {e}")
        return set()

def check_and_index_files(data_folder: str = "data"):
    """Check if all files in the data folder are indexed, and index missing ones."""
    collection = get_collection()
    
    if not os.path.exists(data_folder):
        print(f"⚠️  Data folder '{data_folder}' does not exist.")
        return
    
    data_files = {
        f for f in os.listdir(data_folder) 
        if os.path.isfile(os.path.join(data_folder, f))
    }
    
    if not data_files:
        print(f"⚠️  No files found in '{data_folder}' folder.")
        return
    
    indexed_files = get_indexed_files(collection)
    
    missing_files = data_files - indexed_files
    
    if not missing_files:
        print(f"✅ All files in '{data_folder}' are already indexed in ChromaDB.")
        return
    
    print(f"📝 Found {len(missing_files)} file(s) that need to be indexed:")
    for file in missing_files:
        print(f"   - {file}")
    
    print("\n🔄 Indexing missing files...")
    for file in missing_files:
        file_path = os.path.join(data_folder, file)
        print(f"   Processing: {file}")
        ids, chunks, metadata = _process_document(file_path)
        _add_to_collection(collection, ids, chunks, metadata)
        print(f"   ✓ Indexed: {file} ({len(chunks)} chunks)")
    
    print(f"\n✅ All files in '{data_folder}' are now indexed in ChromaDB.")