import os
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import re
from langchain_core.documents import Document
from app.rag.embeddings import embedding_model
from langchain_community.vectorstores import Chroma
from app.vectorstore.client import get_vectorstore

class ingestionPipeline:
    def __init__(self,documents):
        self.documents=documents
    
    def createDocuments(self,files,file_type):
        for file in files:
            if(file_type == "pdf"):
                loader=PyPDFLoader(str(file))
            elif(file_type=="txt"):
                loader=TextLoader(str(file))
            else:
                raise ValueError("Choose appropriate file type between pdf and txt !")
            documents=loader.load()
            self.all_documents.extend(documents)
        
     

    def normalize_newlines(self,docs, max_newlines=2):
        cleaned_docs = []
        pattern = rf"\n{{{max_newlines+1},}}"

        for doc in docs:
            cleaned_text = re.sub(pattern, "\n" * max_newlines, doc.page_content)
            cleaned_docs.append(
                Document(
                    page_content=cleaned_text,
                    metadata=doc.metadata
                )
            )
        return cleaned_docs
    
    def pipeline(self):
        cleaned_docs=self.normalize_newlines(self.documents,max_newlines=2)
        text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=512,
            chunk_overlap=50
        )
        docs_splits=text_splitter.split_documents(cleaned_docs)
        print("Length of chunks : ",len(docs_splits))
        vectorstore=get_vectorstore()
        vectorstore.add_documents(docs_splits)
        vectorstore.persist()

        print("Documents chunks created and stored in vector DB !")
        return docs_splits

