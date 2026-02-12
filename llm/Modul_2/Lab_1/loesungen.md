# Lab 1: LLMs + eigene Inhalte – Lösungen

## Aufgabe 1 – JSONL vorbereiten

1. **Validierung:** Das CLI‑Tool von OpenAI bereitet die Datei auf und prüft, ob sie korrekt formatiert ist. Der Befehl lautet beispielsweise:

   ```bash
   openai tools fine_tunes.prepare_data -f training_data.jsonl
   ```

   Dabei wird eine neue Datei `training_data_prepared.jsonl` erzeugt und eine Vorschau der Trainingsdaten angezeigt.

2. **Fine‑Tuning starten:** Um das vorbereitete Training zu starten, verwendet man die Modellbezeichnung (`-m`) und die vorbereitete Datei (`-t`):

   ```bash
   openai api fine_tunes.create -t "training_data_prepared.jsonl" -m "gpt-3.5-turbo"
   ```

   OpenAI gibt daraufhin eine Job‑ID aus und nach Abschluss eine Modell‑ID mit dem Präfix `ft:`.

3. **Kostenabschätzung:** 5 000 Tokens ÷ 1 000 × 0,008 USD = **0,04 USD**. Das sind die einmaligen Kosten für das Training (Inferenzen fallen zusätzlich an).

## Aufgabe 2 – Fine‑tuned Modell verwenden

1. **Parametererklärung:**  
   • `model` enthält die ID des feinabgestimmten Modells. Das Präfix `ft:` weist darauf hin, dass es sich um ein Fine‑Tuning einer Basismodel‑Version handelt.  
   • `messages` ist eine Liste aus Nachricht‑Dictionaries. Bei Chat‑Modellen wird zwischen Rollen wie `user`, `system` und `assistant` unterschieden. Im Beispiel wird eine Nutzernachricht mit der Frage an das Modell geschickt.

2. **Code‑Anpassung:**

   ```python
   import openai

   response = openai.ChatCompletion.create(
       model="ft:gpt-3.5-turbo:deine-firma::abc123",
       messages=[{"role": "user", "content": "Welche Zahlungsmethoden bietet ihr an?"}]
   )

   print(response["choices"][0]["message"]["content"])
   ```

3. **Antwort testen ohne Internet:** Da das eigentliche Modell nicht offline verfügbar ist, könnte man einen Unit‑Test schreiben, der das erwartete Verhalten simuliert. Man könnte z. B. eine Funktion erstellen, die bei der Eingabe bestimmter Fragen eine definierte Antwort zurückgibt (Mocking). Alternativ kann man das Fine‑Tuning lokal mit einem kleineren Open‑Source‑Modell nachstellen und dort den Code testen.

## Aufgabe 3 – Einfache RAG‑Pipeline

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Dokument laden
with open("agb_beispiel.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Text in ein Format bringen, das LangChain erwartet
from langchain.schema import Document

documents = [Document(page_content=text)]

# 2. Chunks bilden
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 3. Embeddings erzeugen
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# 4. Vektordatenbank aufbauen
vectordb = FAISS.from_documents(chunks, embedding_model)

# 5. Frage stellen und Top‑3 Dokumente holen
frage = "Welche Rückgabe- und Rückerstattungsbedingungen gelten?"
relevante_docs = vectordb.similarity_search(frage, k=3)
for i, d in enumerate(relevante_docs, 1):
    print(f"Dokument {i}:\n{d.page_content}\n---")

# 6. RetrievalQA-Chain verwenden
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    retriever=vectordb.as_retriever()
)
antwort = qa_chain.run(frage)
print("Antwort:", antwort)
```

**Wann RAG statt Fine‑Tuning?**  
RAG eignet sich besonders dann, wenn deine Wissensbasis häufig aktualisiert wird oder sehr groß ist. Anstatt das Modell für jede Datenänderung neu zu trainieren, lädst du einfach die neuen Dokumente in die Vektordatenbank. Zudem musst du keine proprietären Modelle anpassen und profitierst von geringeren Kosten. Wenn sich die Anfragen jedoch stark ähneln und du immer die gleichen Antworten geben möchtest, kann ein Fine‑Tuning effizienter sein.
