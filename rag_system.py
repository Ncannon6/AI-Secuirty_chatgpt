
from pathlib import Path
import os
import chromadb
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Find the project folder
project_folder = Path(__file__).resolve().parent

# Load the API key
load_dotenv(project_folder / ".env")

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=str(project_folder / "chroma_data")
)

# Use OpenAI to create searchable embeddings
embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# Create the cybersecurity knowledge collection
collection = client.get_or_create_collection(
    name="security_playbooks",
    embedding_function=embedding_function
)

def load_knowledge():
    file_path = project_folder / "knowledge_base" / "brute_force_response.txt"

    with open(file_path, "r") as file:
        document = file.read()

    collection.upsert(
        ids=["brute_force_guide"],
        documents=[document]
    )

    print("Cybersecurity knowledge loaded!")


def search_knowledge(question):
    results = collection.query(
        query_texts=[question],
        n_results=1
    )

    return results["documents"][0][0]


if __name__ == "__main__":
    load_knowledge()

    answer = search_knowledge(
        "How should an analyst investigate repeated failed logins?"
    )

    print(answer)
