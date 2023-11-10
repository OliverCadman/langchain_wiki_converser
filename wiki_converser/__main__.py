from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

import pinecone
from dataclasses import dataclass

import os
from argparse import ArgumentParser



def ingest_docs(subject: str, pinecone_env):
    """Search wikipedia for article based on subject, and load into vectorstore."""
    pinecone.init(api_key=pinecone_env.api_key, environment=pinecone_env.environment_region)
    loader = WikipediaLoader(query=subject, load_max_docs=1)
    raw_text = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    document = text_splitter.split_documents(raw_text)
    embedding = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    
    Pinecone.from_documents(documents=document, embedding=embedding, index_name=pinecone_env.index_name)

    print(f"Successfully loaded {subject} into the vectorstore.")


def run_llm(pinecone_env):
    pinecone.init(api_key=pinecone_env.api_key, environment=pinecone_env.environment_region)

    embedding = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    doc_search = Pinecone.from_existing_index(
        index_name=pinecone_env.index_name,
        embedding=embedding
    )
    
    chat_model = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-3.5-turbo", 
        temperature=1,
        verbose=True
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=doc_search.as_retriever()
    )

    chat_history = []

    print("Start a conversation with me, please. I'm so bored.\n\n")
    while True:
        query = input("You: ")
        if query == "quit":
            break
        response = qa({"question": query, "chat_history": chat_history})
        print(f"Response: {response.get('answer')}\n")
        chat_history.append((query, response))


@dataclass
class PineconeCredentials:
    api_key: str
    index_name: str
    environment_region: str


def init_pinecone():
    api_key = os.environ.get("PINECONE_API_KEY")
    index_name = os.environ.get("PINECONE_INDEX_NAME")
    environment = os.environ.get("PINECONE_ENVIRONMENT_REGION")

    if api_key is None:
        msg = "PINECONE_API_KEY environment variable is not set."
        raise ValueError(msg)
    
    if index_name is None:
        msg = "PINECONE_INDEX_NAME environment variable is not set."
        raise ValueError(msg)
    
    if environment is None:
        msg = "PINECONE_ENVIRONMENT_REGION environment variable is not set."
        raise ValueError(msg)
    
    return PineconeCredentials(
        api_key=api_key,
        index_name=index_name,
        environment_region=environment
    )


if __name__ == "__main__":

    load_dotenv()
    pinecone_env = init_pinecone()

    parser = ArgumentParser(prog="Wikipedia QA", 
                            description="Chatbot that answers questions based on Wikipedia articles.")

    parser.add_argument("--load", type=str, help="Provide a subject to load from Wikipedia")
    parser.add_argument("--chat", action="store_true", help="Converse with the chatbot.")

    args = parser.parse_args()

    if args.load:
        ingest_docs(args.load, pinecone_env)
    else:
        run_llm(pinecone_env)
