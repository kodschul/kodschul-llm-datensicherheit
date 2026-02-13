# Simuliere Dokumente mit Metadaten
from langchain_classic.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

from langchain_classic.chains import RetrievalQA


from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate


llm = Ollama(
    model="llama3.2:1b",
    temperature=0.7,
    num_thread=2
)

docs_with_metadata = [
    Document(
        page_content="Bestellung #12345 (Max): In Bearbeitung",
        metadata={"user_id": "user_123", "type": "order"}
    ),
    Document(
        page_content="Bestellung #12346 (Anna): Versandt",
        metadata={"user_id": "user_456", "type": "order"}
    ),
    Document(
        page_content="Bestellung #12347 (Tom): Storniert",
        metadata={"user_id": "user_789", "type": "order"}
    ),
]
embeddings = OllamaEmbeddings(model="llama3.2:1b")
vector_db = Chroma(embedding_function=embeddings,
                   persist_directory="./db/context_chroma_db")


# Vektordatenbank mit Metadaten erstellen (Hinweis: eigentlich müsstest du diese neu befüllen)
vector_db.add_documents(docs_with_metadata)

# Retriever mit Metadaten-Filter
current_user_id = "user_789"  # Simulierte User-ID

retriever_filtered = vector_db.as_retriever(
    search_kwargs={
        # "k": 4,
        "filter": {"user_id": current_user_id}  # NUR Dokumente dieses Users!
    }
)

# Test
question = "Was ist der Status meiner Bestellung? "
res = retriever_filtered.invoke(question)

print(f"Gefilterte Dokumente (nur user_id={current_user_id}):")
print(res)
# for doc in filtered_docs:
#     print(f"- {doc.page_content}")
#     print(f"  Metadata: {doc.metadata}")

prompt = ChatPromptTemplate.from_template("""
Du bist ein Order-Support Assistent

Kontext:
{context}

Frage:
{input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever_filtered, document_chain)
res = rag_chain.invoke({"input": question})

print(res)
print(res['answer'])
