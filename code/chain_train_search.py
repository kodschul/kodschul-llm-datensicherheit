from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_ollama import OllamaEmbeddings


# dokumente laden


print("loading docs")

loader = DirectoryLoader(
    "data",
    glob="**/*.txt",
    loader_cls=TextLoader
)

documents = loader.load()

print("chunking")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)


print("training")
# index erstellen
embeddings = OllamaEmbeddings(model="llama3.2:1b")


index = Chroma.from_documents(
    documents=chunks, embedding=embeddings, persist_directory="./db/chroma")


print("searching")
res = index.similarity_search("wie kann ich kündigen?")

print(res)

# for r in res:
#     print(r.page_content)
