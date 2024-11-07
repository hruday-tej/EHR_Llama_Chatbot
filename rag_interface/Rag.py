from langchain_community.document_loaders import JSONLoader
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import getpass
import os
import json
from pathlib import Path
from pprint import pprint
import openai
from .constants import Constants


class RAG:

    def is_vector_store_empty(self):

        vector_store_dir = Path(Constants.vector_db_location)

        if vector_store_dir.exists() and vector_store_dir.is_dir():
            return not any(vector_store_dir.iterdir())
        else:
            return True

    def __init__(self):
        # connect to the data source file/vectordb
        api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = OpenAIEmbeddings(model=Constants.open_ai_embedding_model)
        if api_key is None:
            raise ValueError(
                "OpenAI API Key not found. Set the API key before running the script."
            )

        if self.is_vector_store_empty():
            print("Vector store is empty. Building the vector store...")
            self.build_vector_db(
                "/home/hrudayte.akkalad/dev/ehr_pipeline/data_store/raw/qbank.jsonl"
            )
        else:
            print("Vector store already exists and is not empty.")

    def build_vector_db(self, json_list: list):
        # information needs to be passed into the func param
        # build the vector db
        # update the data source
        # Todo : check if the db exists?
        def json_to_document(record):
            text_fields = [
                record.get("question", ""),
                record.get("template", ""),
                record.get("tag", ""),
                record.get("q_tag", ""),
            ]

            content = " ".join(text_fields)

            metadata = {
                "query": record.get("query", ""),
                "db_id": record.get("db_id", ""),
                "id": record.get("id", ""),
            }

            return Document(page_content=content, metadata=metadata)

        with open(json_list, "r") as f:
            records = json.load(f)

        documents = [json_to_document(record) for record in records]
        # print(documents)
        vector_store = FAISS.from_documents(documents, self.embedding_model)
        vector_store.save_local(Constants.vector_db_location)
        # pass

    def retrieve(self, user_query: str):
        vector_store = FAISS.load_local(
            Constants.vector_db_location,
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        k = 3
        matched_docs = vector_store.similarity_search(user_query, k=k)

        return matched_docs[0].metadata["query"]
