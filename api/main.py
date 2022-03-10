from enum import Enum
from typing import Optional
from xmlrpc.client import boolean
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    comment: str


class User(BaseModel):
    name: str
    password: str

class ModelName(str, Enum):
    first = "first"
    second = "second"
    third = "third"


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/post")
def get_post():
    return {"data": "This is a post"}


@app.get("/model/{model_name}")
def get_model(model_name: ModelName):
    if model_name == model_name.first:
        return {"Model Name": f"{model_name}"}
    if model_name == model_name.second:
        return {"Model Name": f"{model_name}"}
    if model_name == model_name.third:
        return {"Model Name": f"{model_name}"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    return {"message": f"title: {payload['title']} - comment: {payload['comment']}"}


@app.get("/user/{user_id}/item/{item_id}")
def read_user_item(user_id: int, item_id: int, q: Optional[str] = Query(None, max_length=50)):
    item = {"user": user_id, "item": item_id}
    if q:
        item.update({"q": q})
    return item
    

@app.get("/sample_post/{post}")
def sample_post(post: str, q: Optional[str] = None, state: boolean = False):
    post = {"Message": post}
    if state:
        post["Message"] = "Message not supported"
    return post
        

@app.get("/user")
def get_user(payload: User):
    return {"Payload": payload}