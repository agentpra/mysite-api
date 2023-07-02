from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
 
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

APP_VERSION = "/api/v1/"
ALLOWED_ORIGINS = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# decorator 
@app.post(APP_VERSION + "user/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user2 = crud.get_user_by_username(db, username=user.username)
    if db_user2:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db=db, user=user)


# login
@app.post(APP_VERSION + "user/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.validate_user(db, user.username, user.password)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid User")
    return db_user


@app.get(APP_VERSION + "users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get(APP_VERSION + "user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(APP_VERSION + "user/{user_id}/posts/")
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.get(APP_VERSION + "posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts


@app.get(APP_VERSION + "suggestions/")
def get_suggestions(user_id: int, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=0, limit=100)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    data = []
    for user in db_users:
        if user.id != user_id:
            data.append(
                {
                    "username": user.username,
                    "fullname": user.fullname,
                    "title": user.title,
                }
            )
    return data

@app.post(APP_VERSION + "posts/update_likes")
def update_post_likes(like_info: schemas.UpdateLikes, db: Session = Depends(get_db)):
    likes = crud.update_post_likes(like_info, db)
    if likes is None:
        raise HTTPException(status_code=404, detail="Unable to update likes")
    return likes

@app.post(APP_VERSION + "posts/update_comment")
def update_post_comments(comment_info: schemas.UpdateComments, db: Session = Depends(get_db)):
    comments = crud.update_post_comments(comment_info, db)
    if comments is None:
        raise HTTPException(status_code=404, detail="Unable to update comments")
    return comments