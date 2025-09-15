from fastapi import APIRouter
import os, json

router = APIRouter(tags=["clinician"])

@router.get("/patients")
async def list_patients():
    base = "./data/patients"
    if not os.path.exists(base):
        return []
    return [d for d in os.listdir(base) if os.path.isdir(os.path.join(base,d))]

@router.get("/patient/{pid}/messages")
async def get_messages(pid: str):
    path = f"./data/patients/{pid}/messages.jsonl"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

@router.get("/patient/{pid}/plan")
async def get_plan(pid: str):
    path = f"./data/patients/{pid}/plan.yaml"
    if not os.path.exists(path):
        return {"plan": None}
    return {"plan": open(path,encoding="utf-8").read()}
