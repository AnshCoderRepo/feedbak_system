from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_manager, require_employee
from app import models, schemas, crud

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/manager", response_model=schemas.ManagerDashboard)
async def get_manager_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_manager)
):
    """Get dashboard data for managers"""
    # Get team members
    team_members = crud.get_team_members(db, current_user.id)
    
    # Get feedback statistics
    total_feedback = len(crud.get_feedback_by_manager(db, current_user.id))
    recent_feedback = crud.get_feedback_by_manager(db, current_user.id)[:5]
    
    # Calculate sentiment distribution
    all_feedback = crud.get_feedback_by_manager(db, current_user.id)
    positive_feedback = len([f for f in all_feedback if f.sentiment == "positive"])
    neutral_feedback = len([f for f in all_feedback if f.sentiment == "neutral"])
    negative_feedback = len([f for f in all_feedback if f.sentiment == "negative"])
    
    return {
        "team_size": len(team_members),
        "team_members": team_members,
        "total_feedback": total_feedback,
        "positive_feedback": positive_feedback,
        "neutral_feedback": neutral_feedback,
        "negative_feedback": negative_feedback,
        "recent_feedback": recent_feedback
    }

@router.get("/employee", response_model=schemas.EmployeeDashboard)
async def get_employee_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_employee)
):
    """Get dashboard data for employees"""
    # Get feedback statistics
    all_feedback = crud.get_feedback_for_employee(db, current_user.id)
    total_feedback = len(all_feedback)
    unacknowledged_feedback = len([f for f in all_feedback if not f.acknowledged])
    recent_feedback = crud.get_recent_feedback_by_employee(db, current_user.id, limit=5)
    positive_feedback = len([f for f in all_feedback if f.sentiment == "positive"])
    neutral_feedback = len([f for f in all_feedback if f.sentiment == "neutral"])
    negative_feedback = len([f for f in all_feedback if f.sentiment == "negative"])
    
    return schemas.EmployeeDashboard(
        total_feedback=total_feedback,
        positive_feedback=positive_feedback,
        neutral_feedback=neutral_feedback,
        negative_feedback=negative_feedback,
        recent_feedback=recent_feedback,
        unacknowledged_feedback=unacknowledged_feedback
    )