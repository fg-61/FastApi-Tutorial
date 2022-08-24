from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
#import uvicorn # for debugging

app = FastAPI()



@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}


# unpublished bir aşağıda olsaydı path çakışması olacaktı
@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data':id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    # fetch comments of blog with id = id
    return {'data': {'1', '2'}}

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return {'data':f'Blog is created wtih title as {request.title}'}

# for debugging
#if __name__ == '__main__':
#   uvicorn.run(app,host="127.0.0.1",port=9000)