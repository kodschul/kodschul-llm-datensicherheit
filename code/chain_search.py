from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_ollama import OllamaEmbeddings

print("load existing index")
# index erstellen
embeddings = OllamaEmbeddings(model="llama3.2:1b")


index = Chroma(embedding_function=embeddings, persist_directory="./db/chroma")


print("searching")
# res = index.similarity_search("wie kann ich kündigen?")
res = index.similarity_search("onboarding neuer Mitarbeiter")


print(res)

# for r in res:
#     print(r.page_content)
