from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, plans, ingest, clinician
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="ADHD Follow-Up API (Local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/v1")
app.include_router(plans.router, prefix="/v1")
app.include_router(ingest.router, prefix="/v1")
app.include_router(clinician.router, prefix="/v1/clinician")

@app.get("/health")
def health():
    return {"ok": True}
