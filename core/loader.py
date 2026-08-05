from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    try:
        loader=PyPDFLoader(file_path)
        documents=loader.load()
        return documents
    except Exception as e:
        raise Exception(f"error loading pdf:{e}")
    