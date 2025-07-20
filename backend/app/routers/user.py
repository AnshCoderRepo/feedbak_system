from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_manager
from app import models, schemas, crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_profile(
    current_user: models.User = Depends(get_current_user)
):
    """Get current user's profile"""
    return current_user

@router.get("/team", response_model=List[schemas.UserResponse])
async def get_team_members(
    current_user: models.User = Depends(require_manager),
    db: Session = Depends(get_db)
):
    """Get team members for the current manager"""
    team_members = crud.get_team_members(db, current_user.id)
    return team_members

@router.get("/managers", response_model=List[schemas.UserResponse])
async def get_managers(db: Session = Depends(get_db)):
    """Get all managers for registration dropdown"""
    managers = crud.get_managers(db)
    return managers

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user_by_id(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (managers can see their team members, employees can see themselves)"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check permissions: managers can see their team members, employees can only see themselves
    if current_user.role.value == "manager":
        # Managers can see their team members
        if user.manager_id != current_user.id and user.id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only view your team members")
    else:
        # Employees can only see themselves
        if user.id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only view your own profile")
    
    return user