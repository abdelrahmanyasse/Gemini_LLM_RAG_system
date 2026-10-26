import chromadb
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("jarvis_knowledge")

query = "what accuracy did the face verification project achieve"
query_embedding = embed_model.encode(query).tolist()

results = collection.query(query_embeddings=[query_embedding], n_results=1)
print(results["documents"])