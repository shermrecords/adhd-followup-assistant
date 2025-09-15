from fastapi import APIRouter

router = APIRouter(tags=["ingest"])

@router.post("/ingest/file")
async def ingest_file():
    return {"ok": True, "message": "File ingestion stub"}
