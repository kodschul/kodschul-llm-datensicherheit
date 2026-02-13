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
                   persist_directory="../../db/chroma")


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


FORBIDDEN_KEYWORDS = ["gehalt", "geburtsdatum", "private", "telefonnummer"]


def is_allowed(query: str):
    return not any(word in query.lower() for word in FORBIDDEN_KEYWORDS)


def ask_ai(query):

    if not is_allowed(query):
        print("Not allowed to ask AI")
        return

    # res = index.similarity_search("wie kann ich kündigen?")
    res = rag_chain.invoke(
        {"input": query})

    print(res)
    print(res['answer'])


ask_ai("welches Gehalt bekommt ein Softwaredeveloper?")
