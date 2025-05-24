import pdfplumber
import requests
import random
import time

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
        return "\n".join(pages)
    except Exception as e:
        return ""

def count_tokens(text):
    return len(text.split())

def generate_mcqs_with_ollama(text_chunk, num_questions, ollama_api_url="http://localhost:11434/v1/chat/completions"):
    prompt = (
        f"Create {num_questions} multiple-choice questions based on the following text:\n\n"
        f"{text_chunk}\n\n"
        "Each question should have four choices, one correct answer and three incorrect answers."
    )
    data = {
        "model": "llama3.2:1b-instruct-q4_0",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    try:
        response = requests.post(ollama_api_url, json=data)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception:
        return None

def generate_mcqs_from_text(text, num_questions, chunk_size=1000, max_retries=5):
    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    mcqs = ""
    retries = 0
    while not mcqs and retries < max_retries:
        chunk = random.choice(text_chunks)
        mcqs = generate_mcqs_with_ollama(chunk, num_questions)
        if not mcqs:
            retries += 1
            time.sleep(1)
    return mcqs

def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=20)
    splits = splitter.split_text(text)
    embeddings = OllamaEmbeddings(model='nomic-embed-text:latest')
    return InMemoryVectorStore.from_texts(splits, embeddings)

def ask_and_get_answer(vector_store, question):
    model = OllamaLLM(model="llama3.2:1b-instruct-q4_0")
    retriever = vector_store.as_retriever()

    template = """
    You are an assistant for question-answering tasks.
    If question is related to provided context use provided context and your knowledge to answer the user question and if the question is not related to given context then do not answer the question:

    <context>
    {context}
    </context>

    Question: {input}
    """

    prompt = ChatPromptTemplate.from_template(template)
    doc_chain = create_stuff_documents_chain(model, prompt)
    chain = create_retrieval_chain(retriever, doc_chain)
    response = chain.invoke({"input": question})

    return response.get('answer', "Sorry, no answer found.")
