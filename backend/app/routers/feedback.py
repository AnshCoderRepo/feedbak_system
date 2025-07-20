from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_manager
from app import models, schemas, crud

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/", response_model=schemas.FeedbackResponse)
async def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_manager)
):
    """Create new feedback (managers only)"""
    # Verify the employee belongs to the manager's team
    employee = crud.get_user(db, feedback.employee_id)
    if not employee or employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create feedback for your team members"
        )
    
    return crud.create_feedback(db, feedback, current_user.id)

@router.get("/", response_model=List[schemas.FeedbackResponse])
async def get_feedback(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get feedback based on user role"""
    if current_user.role.value == models.Role.manager:
        # Managers see all feedback they've given
        return crud.get_feedback_by_manager(db, current_user.id)
    else:
        # Employees see feedback they've received
        return crud.get_feedback_for_employee(db, current_user.id)

@router.get("/my-feedback", response_model=List[schemas.FeedbackResponse])
async def get_my_feedback(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get feedback for the current user (employee view)"""
    return crud.get_feedback_for_employee(db, current_user.id)

@router.get("/{feedback_id}", response_model=schemas.FeedbackResponse)
async def get_feedback_by_id(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get specific feedback by ID"""
    feedback = crud.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Check access permissions
    if current_user.role.value == models.Role.manager and feedback.manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this feedback")
    elif current_user.role.value == models.Role.employee and feedback.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this feedback")
    
    return feedback

@router.put("/{feedback_id}", response_model=schemas.FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    feedback_update: schemas.FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_manager)
):
    """Update feedback (managers only)"""
    feedback = crud.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if feedback.manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own feedback")
    
    return crud.update_feedback(db, feedback_id, feedback_update)

@router.post("/{feedback_id}/acknowledge", response_model=schemas.FeedbackResponse)
async def acknowledge_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Acknowledge feedback (employees only)"""
    feedback = crud.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if current_user.role.value != models.Role.employee:
        raise HTTPException(status_code=403, detail="Only employees can acknowledge feedback")
    
    if feedback.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only acknowledge your own feedback")
    
    return crud.acknowledge_feedback(db, feedback_id)

@router.post("/{feedback_id}/comment", response_model=schemas.FeedbackResponse)
async def add_employee_comment(
    feedback_id: int,
    comment_data: schemas.EmployeeComment,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add employee comment to feedback"""
    feedback = crud.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if current_user.role.value != models.Role.employee:
        raise HTTPException(status_code=403, detail="Only employees can add comments")
    
    if feedback.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only comment on your own feedback")
    
    return crud.add_employee_comment(db, feedback_id, comment_data.comment)

@router.get("/employee/{employee_id}", response_model=List[schemas.FeedbackResponse])
async def get_employee_feedback(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_manager)
):
    """Get feedback for a specific employee (managers only)"""
    # Verify the employee is managed by current user
    employee = crud.get_user(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if employee.manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view feedback for your team members")
    
    return crud.get_feedback_for_employee(db, employee_id)