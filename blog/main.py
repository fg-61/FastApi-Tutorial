from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with the id:{id} is not available')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)(synchronize_session=False)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with the id:{id} is not available')
    blog.delete()
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id:{id} not found")

    blog.update(request.dict())
    db.commit()
    return request


# User



@app.post('/user', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name,
                           email = request.email, 
                           password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user_by_id(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id:{id} is not available')
    return user