"""
Task Model - SQLAlchemy ORM Model for Tasks

Demonstrates:
- SQLAlchemy declarative models
- Relationship definitions
- Enum types for status/priority
- Timestamps and soft delete
- Field validation
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    """
    Task database model.
    
    Attributes:
        id: Primary key
        title: Task title (required)
        description: Detailed description
        status: Current status (enum)
        priority: Priority level (enum)
        due_date: Optional due date
        owner_id: Foreign key to User
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        is_deleted: Soft delete flag
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )
    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False
    )
    due_date = Column(DateTime, nullable=True)
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
    
    def soft_delete(self):
        """Perform soft delete on the task."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        """Restore a soft-deleted task."""
        self.is_deleted = False
        self.deleted_at = None
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status != TaskStatus.COMPLETED:
            return datetime.utcnow() > self.due_date
        return False
