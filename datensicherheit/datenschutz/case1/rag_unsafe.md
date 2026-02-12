
# RAG mit Ollama - Hands-on Beispiel (ohne Datenschutzmaßnahmen)

## Setup

```bash
# Ollama installieren und starten
ollama pull mistral
ollama pull nomic-embed-text
```

## 1. Chunking & Embeddings

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Beispieltext
content = """
Die DSGVO regelt den Datenschutz in der EU.
Personendaten müssen geschützt werden.
Nutzer haben Rechte auf ihre Daten.
"""

# Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text(content)

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = FAISS.from_texts(chunks, embeddings)
```

## 2. Erste RAG-Abfrage

```python
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

llm = Ollama(model="mistral")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

result = qa.run("Welche Rechte haben Nutzer?")
print(result)
```

## ⚠️ Sicherheitslücken (bewusst!)

- Keine Verschlüsselung
- Keine Zugriffskontrolle
- Daten im RAM/Klartext
- Keine Logging/Auditing
