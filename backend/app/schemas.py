from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    name: str
    email: str
    role: str  # "manager" or "employee"

class UserCreate(UserBase):
    password: str
    manager_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    manager_id: Optional[int] = None
    manager: Optional['UserResponse'] = None
    
    class Config:
        from_attributes = True

class User(UserResponse):
    pass

# Auth schemas
class LoginCredentials(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Feedback schemas
class FeedbackBase(BaseModel):
    strengths: str
    areas_to_improve: str
    sentiment: str  # "positive", "neutral", "negative"
    tags: Optional[List[str]] = []
    is_anonymous: bool = False

class FeedbackCreate(FeedbackBase):
    employee_id: int

class FeedbackUpdate(BaseModel):
    strengths: Optional[str] = None
    areas_to_improve: Optional[str] = None
    sentiment: Optional[str] = None
    tags: Optional[List[str]] = None
    is_anonymous: Optional[bool] = None

class FeedbackResponse(FeedbackBase):
    id: int
    employee_id: int
    manager_id: int
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None
    employee_comment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee: Optional[UserResponse] = None
    manager: Optional[UserResponse] = None
    
    @property
    def tags(self) -> List[str]:
        if hasattr(self, '_tags'):
            return self._tags
        if isinstance(self.__dict__.get('tags'), str):
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return self.__dict__.get('tags') or []
    
    @tags.setter
    def tags(self, value):
        if isinstance(value, str):
            self._tags = [tag.strip() for tag in value.split(',') if tag.strip()]
        elif isinstance(value, list):
            self._tags = value
        else:
            self._tags = []
    
    class Config:
        from_attributes = True
        json_encoders = {
            list: lambda v: v  # Ensure lists are properly serialized
        }

class Feedback(FeedbackResponse):
    pass

class EmployeeComment(BaseModel):
    comment: str

# Dashboard schemas
class ManagerDashboard(BaseModel):
    team_size: int
    team_members: List[UserResponse]
    total_feedback: int
    positive_feedback: int
    neutral_feedback: int
    negative_feedback: int
    recent_feedback: List[FeedbackResponse]

class EmployeeDashboard(BaseModel):
    total_feedback: int
    unacknowledged_feedback: int