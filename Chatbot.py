import re
import unicodedata
import os
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    system_instruction="You are Jarvis, a helpful and friendly assistant. Use the provided context to answer questions about Abdelrahman when relevant."
)
chat = model.start_chat(history=[])

# RAG setup - local embeddings, no API quota needed
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("jarvis_knowledge")

exits = ["exit", "quit", "goodbye", "bye", "end chat", "ciao"]

def sanitize(user_input):
    user_input = user_input.strip()
    user_input = re.sub(r'[\x00-\x1F\x7F]', '', user_input)
    user_input = re.sub(r'\s+', ' ', user_input)
    user_input = re.sub(r'[^\w\s]', '', user_input)
    user_input = unicodedata.normalize('NFKC', user_input)
    user_input = user_input.lower()
    return user_input

def retrieve_context(query, top_k=3):
    query_embedding = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return "\n".join(results["documents"][0])

def build_prompt(user_query, context):
    return f"""Use the following context to answer the question if relevant. If the context doesn't contain the answer, answer normally using your own knowledge.

Context:
{context}

Question: {user_query}"""

while True:
    user_input = input("You: ")
    sanitized = sanitize(user_input)

    if sanitized in exits:
        print("Jarvis: Goodbye!")
        break

    context = retrieve_context(sanitized)
    augmented_prompt = build_prompt(user_input, context)

    response = chat.send_message(augmented_prompt)
    print(f"Jarvis: {response.text}")