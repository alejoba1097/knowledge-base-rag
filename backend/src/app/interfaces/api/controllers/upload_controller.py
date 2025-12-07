from fastapi import HTTPException, UploadFile

from app.application.upload_document import UploadDocumentUseCase


async def handle_upload(
    file: UploadFile,
    use_case: UploadDocumentUseCase,
) -> dict[str, str]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    data = await file.read()
    doc_id = use_case.embed_and_store(filename=file.filename, data=data)

    return {"document_id": doc_id, "status": "indexed", "filename": file.filename}
