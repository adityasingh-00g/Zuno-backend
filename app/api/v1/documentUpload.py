from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
import tempfile
import os
from app.services.ingestion import ingestionPipeline

router = APIRouter()
SUPPORTED_EXTENSIONS = (".pdf", ".txt")


async def read_file(file: UploadFile) -> list[Document]:
    filename = file.filename.lower()

    if not filename.endswith(SUPPORTED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.filename}"
        )

    suffix = ".pdf" if filename.endswith(".pdf") else ".txt"

    try:
        # Save file temporarily (async-safe)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            if not contents:
                raise HTTPException(status_code=400, detail="File is empty")

            tmp.write(contents)
            tmp_path = tmp.name

        # Load document
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)

        documents = loader.load()

        # Add metadata (VERY IMPORTANT for RAG)
        for doc in documents:
            doc.metadata.update({
                "source": file.filename,
                "file_type": suffix.replace(".", "")
            })

        return documents

    finally:
        # Ensure temp file cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/documents/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    all_documents = []
    uploaded_files = []

    try:
        for file in files:
            docs = await read_file(file)
            all_documents.extend(docs)
            uploaded_files.append(file.filename)

        if not all_documents:
            raise HTTPException(status_code=400, detail="No valid content found")

        # Run ingestion once for all docs (efficient)
        ingestion_pipeline = ingestionPipeline(all_documents)
        ingestion_pipeline.pipeline()

        return JSONResponse(
            content={
                "message": "Documents uploaded and indexed successfully",
                "files": uploaded_files,
                "total_chunks": len(all_documents)
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        print("Upload error:", e)
        raise HTTPException(status_code=500, detail="Failed to process documents")
