from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def validate_user(db: Session, username: str, password: str):
    return ( 
        db.query(models.User) 
        .filter(models.User.username == username)
        .filter(models.User.password == password)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

 
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password=user.password,
        username=user.username,
        fullname=user.fullname,
        title=user.title,
        skills=user.skills,
        address=user.address,
        followers=[],
        followings=[],
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(
            models.Post.id,
            models.Post.title,
            models.Post.location,
            models.Post.job_type,
            models.Post.pay_rate_per_hr_dollar,
            models.Post.skills,
            models.Post.liked_by,
            models.Post.viewed_by,
            models.Post.user_id,
            models.Post.description,
            models.Post.comments,
            models.Post.created_at.label("post_date"),
            models.User.username.label("post_by_username"),
            models.User.fullname.label("post_by_fullname"),
        )
        .join(models.User)
        .offset(skip)
        .limit(limit)
        .all()
    ) 


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post_likes(like_info, db: Session):
    post = db.query(models.Post).filter(models.Post.id==like_info.post_id).first()
    user = db.query(models.User).filter(models.User.id == like_info.user_id).first()
    new_liked_by = list(post.liked_by)
    if (user.username in new_liked_by):
        new_liked_by.remove(user.username)
    else:
        new_liked_by.append(user.username)
    post.liked_by = new_liked_by;
    db.add(post)
    db.commit()
    db.refresh(post)
    return post.liked_by

def update_post_comments(comment_info, db: Session):
    post = db.query(models.Post).filter(models.Post.id==comment_info.post_id).first()
    user = db.query(models.User).filter(models.User.id == comment_info.user_id).first()
    new_comment = {"username": user.username, "fullname": user.fullname, "comment": comment_info.comment}
    current_comments = list(post.comments)
    current_comments.append(new_comment)
    post.comments = current_comments;
    db.add(post)
    db.commit()
    db.refresh(post)
    return post.comments