from pydantic import BaseModel

class PlanIn(BaseModel):
    patient_id: str
    yaml: str

class PlanOut(BaseModel):
    ok: bool
    message: str
