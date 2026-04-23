from pydantic import BaseModel, Field
from typing import List, Optional

class Clause(BaseModel):
    clause_id: str
    title: str
    content: str

class LegalReference(BaseModel):
    section: str
    content: str

class AuditDetail(BaseModel):
    clause_id: str
    risk_level: str
    reason: str
    suggestion: str
    references: List[LegalReference] = []

class FinalAuditReport(BaseModel):
    report_id: str
    filename: str
    overall_status: str
    details: List[AuditDetail]