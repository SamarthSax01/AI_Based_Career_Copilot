from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
def get_document_chain(llm,prompt):
    document_chain=create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )
    return document_chain
def get_retrieval_chain(retriever,document_chain):
    retriever_chain=create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain
    )
    return retriever_chain
def build_rag_chain(llm,retriever,prompt):
    document_chain=get_document_chain(
        llm=llm,
        prompt=prompt
    )
    retrieval_chain=get_retrieval_chain(
        retriever,
        document_chain
    )
    return retrieval_chain

