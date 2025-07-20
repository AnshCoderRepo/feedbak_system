from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas
from datetime import datetime
from sqlalchemy import and_, desc

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=models.UserRole(user.role),
        manager_id=user.manager_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_team_members(db: Session, manager_id: int) -> List[models.User]:
    """Get all team members for a specific manager"""
    return db.query(models.User).filter(models.User.manager_id == manager_id).all()

def get_managers(db: Session) -> List[models.User]:
    """Get all users with manager role"""
    return db.query(models.User).filter(models.User.role == models.UserRole.MANAGER).all()

# Feedback CRUD operations
def create_feedback(db: Session, feedback: schemas.FeedbackCreate, manager_id: int) -> models.Feedback:
    """Create new feedback"""
    db_feedback = models.Feedback(
        employee_id=feedback.employee_id,
        manager_id=manager_id,
        strengths=feedback.strengths,
        areas_to_improve=feedback.areas_to_improve,
        sentiment=feedback.sentiment,
        tags=",".join(feedback.tags) if feedback.tags else "",
        is_anonymous=feedback.is_anonymous
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session, feedback_id: int) -> Optional[models.Feedback]:
    """Get feedback by ID"""
    return db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()

def get_feedback_for_employee(db: Session, employee_id: int) -> List[models.Feedback]:
    """Get all feedback for a specific employee"""
    return db.query(models.Feedback).filter(models.Feedback.employee_id == employee_id).order_by(desc(models.Feedback.created_at)).all()

def get_feedback_by_manager(db: Session, manager_id: int) -> List[models.Feedback]:
    """Get all feedback created by a specific manager"""
    return db.query(models.Feedback).filter(models.Feedback.manager_id == manager_id).order_by(desc(models.Feedback.created_at)).all()

def update_feedback(db: Session, feedback_id: int, feedback_update: schemas.FeedbackUpdate) -> Optional[models.Feedback]:
    """Update existing feedback"""
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        return None
    
    update_data = feedback_update.dict(exclude_unset=True)
    if 'tags' in update_data and update_data['tags']:
        update_data['tags'] = ",".join(update_data['tags'])
    
    for field, value in update_data.items():
        setattr(db_feedback, field, value)
    
    db_feedback.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def acknowledge_feedback(db: Session, feedback_id: int) -> Optional[models.Feedback]:
    """Mark feedback as acknowledged"""
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        return None
    
    db_feedback.acknowledged = True
    db_feedback.acknowledged_at = datetime.now()
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def add_employee_comment(db: Session, feedback_id: int, comment: str) -> Optional[models.Feedback]:
    """Add employee comment to feedback"""
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        return None
    
    db_feedback.employee_comment = comment
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# Dashboard helper functions
def get_feedback_stats(db: Session, user_id: int, is_manager: bool = False) -> dict:
    """Get feedback statistics for dashboard"""
    if is_manager:
        # Manager sees stats for feedback they've given
        feedback_query = db.query(models.Feedback).filter(models.Feedback.manager_id == user_id)
    else:
        # Employee sees stats for feedback they've received
        feedback_query = db.query(models.Feedback).filter(models.Feedback.employee_id == user_id)
    
    all_feedback = feedback_query.all()
    
    return {
        "total_feedback": len(all_feedback),
        "positive_feedback": len([f for f in all_feedback if f.sentiment == models.FeedbackSentiment.POSITIVE]),
        "neutral_feedback": len([f for f in all_feedback if f.sentiment == models.FeedbackSentiment.NEUTRAL]),
        "negative_feedback": len([f for f in all_feedback if f.sentiment == models.FeedbackSentiment.NEGATIVE]),
        "recent_feedback": feedback_query.order_by(desc(models.Feedback.created_at)).limit(5).all(),
        "unacknowledged_feedback": len([f for f in all_feedback if not f.acknowledged]) if not is_manager else 0
    }