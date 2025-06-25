from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

embeddings = OpenAIEmbeddings()

video_url = "https://youtu.be/-Osca2Zax4Y?si=iyOiePxzUy_bUayO"

def create_vector_db_from_youtube_url(video_url : str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings)
    return db

def get_response_from_query(db, query, memory, k = 4):
    # text-davinci can handle 4097 tokens

    docs = db.similarity_search(query, k = k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(model = "gpt-3.5-turbo")

    prompt = PromptTemplate(
        input_variables = ['question', "docs"],
        template = """
              You are a helpful YouTube assistant that can answer questions about videos
              based on the videos transcript.

              Answer the following questions : {question}
              By searching the following video transcript : {docs}

              Only use the factual information from the transcript to answer the question.

              If you feel like you don't have enough information to answer the question, say "I don't know".

              Yours answers should be detailed.
        """,
    )

    chain = LLMChain(llm = llm, prompt = prompt, memory = memory)
    response_dict = chain.invoke({"question": query, "docs": docs_page_content})
    response_text = response_dict["text"].replace("\n", " ")
    return response_text, docs
    
def generate_quiz_questions(db, num_questions=5):
     # Use top k transcript chunks to build context
    docs = db.similarity_search("", k=8)  # Empty query fetches top 8 chunks

    combined_text = " ".join([doc.page_content for doc in docs])

    prompt = PromptTemplate(
        input_variables=["transcript", "num_questions"],
        template="""
        You are a helpful quiz generator. Your task is to create a quiz from the following YouTube video transcript.

        Transcript:
        {transcript}

        Generate {num_questions} quiz questions that test comprehension. Mix open-ended and multiple choice questions. Format like:

        1. [Question]
        a. Option A
        b. Option B
        c. Option C
        d. Option D
        Answer: [Correct Option or Answer]

        Keep the questions clear and factual.
            """
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.invoke({"transcript": combined_text, "num_questions": num_questions})
    return response["text"]
