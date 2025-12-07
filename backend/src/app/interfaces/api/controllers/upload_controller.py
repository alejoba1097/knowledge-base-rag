import logging

from fastapi import HTTPException, UploadFile

from app.application.upload_document import UploadDocumentUseCase

logger = logging.getLogger(__name__)


async def handle_upload(
    file: UploadFile,
    use_case: UploadDocumentUseCase,
) -> dict[str, str]:
    logger.info("Received upload request: filename=%s content_type=%s", file.filename, file.content_type)
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    data = await file.read()
    logger.info("Read %d bytes for filename=%s", len(data), file.filename)

    doc_id = use_case.embed_and_store(filename=file.filename, data=data)

    logger.info("Upload pipeline completed: filename=%s document_id=%s", file.filename, doc_id)

    return {"document_id": doc_id, "status": "indexed", "filename": file.filename}
