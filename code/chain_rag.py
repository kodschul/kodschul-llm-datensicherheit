from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import OllamaEmbeddings

from langchain_classic.chains import RetrievalQA


from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

print("load existing index")
# index erstellen
embeddings = OllamaEmbeddings(model="llama3.2:1b")

llm = Ollama(
    model="llama3.2:1b",
    temperature=0.7,
    num_thread=2
)

vector_db = Chroma(embedding_function=embeddings,
                   persist_directory="./db/chroma")


prompt = ChatPromptTemplate.from_template("""
Du bist ein Support-Agent.

Beantworte die Frage ausschließlich anhand des folgenden Kontexts.
Falls die Antwort nicht im Kontext steht, sage:
"Diese Information ist nicht in der Wissensdatenbank enthalten."

Gebe dem Kunden nette und ausführliche volle Sätze antworten

Kontext:
{context}

Frage:
{input}
""")

print("asking")
document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

# res = index.similarity_search("wie kann ich kündigen?")
res = rag_chain.invoke({"input": "wie kann ich mein Account hacken?"})


print(res)
print(res['answer'])

# for r in res:
#     print(r.page_content)
