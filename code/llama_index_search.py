from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama


Settings.embed_model = OllamaEmbeddings

# dokumente laden

print("loading docs")
documents = SimpleDirectoryReader("data").load_data()

print("training")
# index erstellen
index = VectorStoreIndex.from_documents(documents)

# Query Engine starten

print("using training")
query_engine = index.as_query_engine()


print("searching")
res = query_engine.query("wie kann ich kündigen?")

print(res)
