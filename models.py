from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship
import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=8), unique=True, index=True)
    email = Column(String(length=30), unique=True, index=True)
    fullname = Column(String(length=20))
    title = Column(String(length=50))
    address = Column(String(length=100))
    skills = Column(JSON)
    password = Column(String(length=8))
    is_active = Column(Boolean, default=True)
    followers = Column(JSON)
    followings = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=50), index=True)
    description = Column(String(length=256), index=True)
    job_type = Column(String(length=30))  # Part Time, Full Time
    pay_rate_per_hr_dollar = Column(Integer)  # 30 /hr
    skills = Column(JSON)
    location = Column(String(length=100))
    liked_by = Column(JSON,nullable=True, default=[])
    comments = Column(JSON, nullable=True, default=[])
    viewed_by = Column(JSON,nullable=True, default=[])
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="posts")