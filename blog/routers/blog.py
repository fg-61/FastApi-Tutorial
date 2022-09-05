from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/blog",
    tags=['blogs']
)
get_db = database.get_db




@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with the id:{id} is not available')
    return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)(synchronize_session=False)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with the id:{id} is not available')
    blog.delete()
    db.commit()
    return 'done'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id:{id} not found")

    blog.update(request.dict())
    db.commit()
    return request