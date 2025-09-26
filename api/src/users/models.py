from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.core.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    workflows = relationship("Workflow", back_populates="owner")
