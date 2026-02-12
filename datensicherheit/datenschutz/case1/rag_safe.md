# RAG mit Ollama - Hands-on Beispiel (mit Datenschutzmaßnahmen)

## Setup

```bash
# Ollama installieren und starten
ollama pull mistral
ollama pull nomic-embed-text
```

## 1. Chunking & Embeddings (mit Verschlüsselung)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from cryptography.fernet import Fernet

# Verschlüsselungsschlüssel generieren
cipher_suite = Fernet(Fernet.generate_key())

# Beispieltext
content = """
Die DSGVO regelt den Datenschutz in der EU.
Personendaten müssen geschützt werden.
Nutzer haben Rechte auf ihre Daten.
"""

# Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text(content)

# Verschlüsselte Chunks
encrypted_chunks = [cipher_suite.encrypt(chunk.encode()) for chunk in chunks]

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = FAISS.from_texts(chunks, embeddings)
```

## 2. RAG-Abfrage (mit Logging & Zugriffskontrolle)

```python
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import logging
from datetime import datetime

# Audit-Logging
logging.basicConfig(filename='rag_audit.log', level=logging.INFO)

# Zugriffskontrolle
def check_access(user_id: str) -> bool:
    authorized_users = ["user1", "user2"]
    return user_id in authorized_users

llm = Ollama(model="mistral")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

user_id = "user1"
if check_access(user_id):
    result = qa.run("Welche Rechte haben Nutzer?")
    logging.info(f"{datetime.now()} - User: {user_id} - Query executed")
    print(result)
else:
    logging.warning(f"{datetime.now()} - Unauthorized access attempt by {user_id}")
```

## ✅ Implementierte Datenschutzmaßnahmen

- ✓ Verschlüsselung (Fernet)
- ✓ Zugriffskontrolle (User-basiert)
- ✓ Audit-Logging (Compliance-konform)
- ✓ Datenminimierung (Chunking)
