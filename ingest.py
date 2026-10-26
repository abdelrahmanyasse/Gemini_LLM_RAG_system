import os 
import chromadb
from sentence_transformers import SentenceTransformer
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def embed_text(text):
    return embed_model.encode(text).tolist()

def main():
    documents = load_documents("data/knowledge_base")
    print(f"Loaded {len(documents)} documents.")
    
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)
    print(f"Splitted into {len(all_chunks)} chunks.")
    
    chroma_client  = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("jarvis_knowledge")
    for i, chunk in enumerate(all_chunks):
        embedding = embed_text(chunk)
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
        print(f"Stored Chunks_{i}")
    print("ingestion completed")
        
if __name__ == "__main__":
    main()
    