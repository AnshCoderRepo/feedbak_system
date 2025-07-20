from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(enum.Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"

class FeedbackSentiment(enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    manager = relationship("User", remote_side=[id], back_populates="team_members")
    team_members = relationship("User", back_populates="manager")
    
    # Feedback relationships
    feedback_given = relationship("Feedback", foreign_keys="Feedback.manager_id", back_populates="manager")
    feedback_received = relationship("Feedback", foreign_keys="Feedback.employee_id", back_populates="employee")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strengths = Column(Text, nullable=False)
    areas_to_improve = Column(Text, nullable=False)
    sentiment = Column(Enum(FeedbackSentiment), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    
    # Optional fields for bonus features
    tags = Column(String(200), nullable=True)  # Comma-separated tags
    is_anonymous = Column(Boolean, default=False)
    employee_comment = Column(Text, nullable=True)
    
    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="feedback_received")
    manager = relationship("User", foreign_keys=[manager_id], back_populates="feedback_given")