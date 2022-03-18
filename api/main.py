from enum import Enum
from os import stat
from typing import Optional
from xmlrpc.client import boolean
from fastapi import Body, Cookie, FastAPI, Query, Path, Header, status, Form
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


class Payment(BaseModel):
    amount: float
    currency: str
    first_name: str
    last_name: str


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to my API"}


@app.post(".login", status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return {"Username": username, "Password": password}

@app.get("/post", status_code=status.HTTP_200_OK)
def get_post():
    return {"data": "This is a post"}


@app.get("/model/{model_name}", status_code=status.HTTP_200_OK)
def get_model(model_name: ModelName):
    if model_name == model_name.first:
        return {"Model Name": f"{model_name}"}
    if model_name == model_name.second:
        return {"Model Name": f"{model_name}"}
    if model_name == model_name.third:
        return {"Model Name": f"{model_name}"}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(payload: dict = Body(...)):
    return {"message": f"title: {payload['title']} - comment: {payload['comment']}"}


@app.get("/user/{user_id}/item/{item_id}", status_code=status.HTTP_200_OK)
def read_user_item(user_id: int, item_id: int, q: Optional[str] = Query(None, max_length=50)):
    item = {"user": user_id, "item": item_id}
    if q:
        item.update({"q": q})
    return item
    

@app.get("/sample_post/{post}", status_code=status.HTTP_200_OK)
def sample_post(*, post: str = Path(..., title="The ID of post to get"), q: Optional[str] = None, state: boolean = False):
    post = {"Message": post}
    if state:
        post["Message"] = "Message not supported"
    return post
        

@app.get("/user", status_code=status.HTTP_200_OK)
def get_user(payload: User):
    return {"Payload": payload}


@app.get("/getCookie/", status_code=status.HTTP_200_OK)
async def getCookie(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


@app.get("/getHeader/", status_code=status.HTTP_200_OK)
async def getCookie(user_agent: Optional[str] = Header(None)):
    return {"user_agent": user_agent}


@app.get("/getPayement/", response_model=Payment, status_code=status.HTTP_200_OK)
def getPayement(pay: Payment):
    return pay