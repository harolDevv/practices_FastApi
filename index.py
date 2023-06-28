# importo fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4


# ejecuto FstAPI y lo guardo en la variable app
app = FastAPI()


# post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


# se define la "base de datos"
posts = []


# definimos ruta en la raiz GET
@app.get('/')
def read_root():
    return {"welcome": "Welcome my api"}  # devolvemos un json


@app.get('/posts')  # ruta para devolver todos los posts 'arreglo de posts'
def get_posts():
    return posts


# ruta para crear un post recibiendo el post desde el cuerpo'
@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid4())
    posts.append(post.dict())
    return post.dict()


# ruta para buscar post por su id'
@app.get('/posts/{post_id}')
def get_post_byId(post_id: str):
    PostById = list(filter(lambda post: post["id"] == post_id, posts))
    if PostById:
        return PostById
    else:
        raise HTTPException(status_code=404, detail='Post not found')


# ruta para eliminar post por su id'
@app.delete('/posts/{post_id}')
def delete_post_byId(post_id: str):
    PostDeleted = list(filter(lambda post: post["id"] == post_id, posts))
    # tengo que evitar la reasignacion cuando en el mismo filter estoy usando ese mismo arreglo
    posts_filtered = list(filter(lambda post: post["id"] != post_id, posts))
    if PostDeleted:
        # Eliminar todos los elementos de la lista original
        posts.clear()
        # Agregar los elementos filtrados a la lista original
        posts.extend(posts_filtered)
        return PostDeleted
    else:
        raise HTTPException(
            status_code=404, detail='Post not found for delete')


# ruta para actualizar un post

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatePost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index].update(updatePost)
            return {"message": "Update successfully"}
    raise HTTPException(status_code=404, detail="Post not found for update")
