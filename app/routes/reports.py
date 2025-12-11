from fastapi import APIRouter, HTTPException, Depends, Query, Request
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from beanie import PydanticObjectId

from app.models.report import IncidentReport, Reporter, AdminNote, ImpactLevel, ReportStatus
from app.models.user import User, UserRole
from app.models.activity import ActionType, TargetType
from app.auth import get_current_user, require_role
from app.utils.activity_logger import log_activity
from app.utils.security import decode_access_token

router = APIRouter()


# Request/Response Models
class CreateReportRequest(BaseModel):
    featureId: Optional[str] = None
    reporterName: str
    reporterEmail: Optional[str] = None
    impactLevel: ImpactLevel = ImpactLevel.MEDIUM
    description: str


class UpdateStatusRequest(BaseModel):
    status: ReportStatus


class AddNoteRequest(BaseModel):
    note: str


class ReportResponse(BaseModel):
    id: str
    featureId: Optional[str] = None
    reporter: Reporter
    impactLevel: str
    description: str
    status: str
    createdAt: datetime
    resolvedAt: Optional[datetime] = None
    adminNotes: List[AdminNote] = []


def report_to_response(report: IncidentReport) -> ReportResponse:
    """Convert IncidentReport document to response model"""
    return ReportResponse(
        id=str(report.id),
        featureId=str(report.featureId) if report.featureId else None,
        reporter=report.reporter,
        impactLevel=report.impactLevel.value,
        description=report.description,
        status=report.status.value,
        createdAt=report.createdAt,
        resolvedAt=report.resolvedAt,
        adminNotes=report.adminNotes
    )


# POST /api/reports - Create report (Any user, extract from token if auth)
@router.post("/", response_model=ReportResponse)
async def create_report(data: CreateReportRequest, request: Request):
    """Create a new incident report. Works for any user (auth optional)."""
    
    # Try to extract user from token if present
    user_id = None
    token = request.cookies.get("auth-token")
    if token:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
    
    reporter = Reporter(
        id=PydanticObjectId(user_id) if user_id else None,
        name=data.reporterName,
        email=data.reporterEmail
    )
    
    report = IncidentReport(
        featureId=PydanticObjectId(data.featureId) if data.featureId else None,
        reporter=reporter,
        impactLevel=data.impactLevel,
        description=data.description,
        status=ReportStatus.PENDING
    )
    await report.insert()
    
    # Log activity if user is authenticated
    if user_id:
        user = await User.get(user_id)
        if user:
            await log_activity(
                user=user,
                action=ActionType.REPORT_CREATED,
                target_type=TargetType.REPORT,
                target_id=report.id,
                target_name=data.description[:50]  # First 50 chars as name
            )
    
    return report_to_response(report)


# GET /api/reports - List reports (Manager only, with filters)
@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    status: Optional[str] = Query(None, description="Filter by status (comma-separated: pending,acknowledged)"),
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """List all incident reports with optional status filter. Manager only."""
    
    if status:
        statuses = [s.strip() for s in status.split(",")]
        reports = await IncidentReport.find(
            {"status": {"$in": statuses}}
        ).sort("-createdAt").to_list()
    else:
        reports = await IncidentReport.find_all().sort("-createdAt").to_list()
    
    return [report_to_response(r) for r in reports]


# PATCH /api/reports/:id/status - Update status (Manager only)
@router.patch("/{report_id}/status", response_model=ReportResponse)
async def update_report_status(
    report_id: str,
    data: UpdateStatusRequest,
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """Update report status. Manager only."""
    
    try:
        report = await IncidentReport.get(PydanticObjectId(report_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    old_status = report.status
    report.status = data.status
    
    # Set resolvedAt if addressing
    if data.status == ReportStatus.ADDRESSED:
        report.resolvedAt = datetime.utcnow()
    
    await report.save()
    
    # Log activity
    action = ActionType.REPORT_ACKNOWLEDGED if data.status == ReportStatus.ACKNOWLEDGED else ActionType.REPORT_ADDRESSED
    await log_activity(
        user=current_user,
        action=action,
        target_type=TargetType.REPORT,
        target_id=report.id,
        target_name=report.description[:50],
        details={"oldStatus": old_status.value, "newStatus": data.status.value}
    )
    
    return report_to_response(report)


# POST /api/reports/:id/notes - Add admin note (Manager only)
@router.post("/{report_id}/notes", response_model=ReportResponse)
async def add_report_note(
    report_id: str,
    data: AddNoteRequest,
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """Add an admin note to a report. Manager only."""
    
    try:
        report = await IncidentReport.get(PydanticObjectId(report_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    note = AdminNote(
        authorId=current_user.id,
        authorName=current_user.name,
        note=data.note
    )
    report.adminNotes.append(note)
    await report.save()
    
    # Log activity
    await log_activity(
        user=current_user,
        action=ActionType.REPORT_NOTE_ADDED,
        target_type=TargetType.REPORT,
        target_id=report.id,
        target_name=report.description[:50]
    )
    
    return report_to_response(report)


# DELETE /api/reports/:id - Delete spam (Manager only)
@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """Delete a spam/invalid report. Manager only."""
    
    try:
        report = await IncidentReport.get(PydanticObjectId(report_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report_desc = report.description[:50]
    await report.delete()
    
    # Log activity
    await log_activity(
        user=current_user,
        action=ActionType.REPORT_DELETED,
        target_type=TargetType.REPORT,
        target_id=PydanticObjectId(report_id),
        target_name=report_desc
    )
    
    return {"message": "Report deleted successfully", "id": report_id}
