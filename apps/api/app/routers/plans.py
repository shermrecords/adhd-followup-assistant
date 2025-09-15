from fastapi import APIRouter
from app.schemas.plan import PlanIn, PlanOut
import os

router = APIRouter(tags=["plans"])

@router.post("/plans", response_model=PlanOut)
async def upsert_plan(body: PlanIn):
    folder = f"./data/patients/{body.patient_id}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/plan.yaml","w",encoding="utf-8") as f:
        f.write(body.yaml)
    return {"ok": True, "message": "Plan stored."}
