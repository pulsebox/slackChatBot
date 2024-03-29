# llamaIndex.py uses the llamaIndex system to create an index of the documents in /documents and saves them in /storage. It then uses the index to retrieve the most relevant documents for a given query. 
# The query_index function takes a retriever and a query as input and returns a string of the retrieved document text. 
# The create_index function checks if the index exists and creates it if it doesn't. If the index exists, it loads the existing index. 

import os.path

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.prompts import PromptTemplate

# check if index exists and create it if it doesn't
def create_index():
    if not os.path.exists("./storage"):
        # load the documents and create the index
        print("creating new index")

        documents = SimpleDirectoryReader("documents").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist()
        retriever = index.as_retriever()
        return retriever
    else:
        # load the existing index
        print("loading existing index")
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
        retriever = index.as_retriever()
        return retriever

# query the retriever
def query_index(retriever, query):
    nodes = retriever.retrieve(query)
    context_str = "\n\n".join([n.node.get_content() for n in nodes])
    # retun a string of retrieved document text
    return context_str

# format the retrieved documents
def format_retrieved_documents(retrieved_documents):
    formatted_documents = ""
    for i, doc in enumerate(retrieved_documents):
        formatted_documents += f"Document {i + 1}:\n{doc}\n\n"
    return formatted_documents

qa_prompt = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)

# create the prompt template for the chatbot
def create_prompt(context_str, query_str):
    return qa_prompt.format(context_str=context_str, query_str=query_str)