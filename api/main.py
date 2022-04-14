from email import header
from enum import Enum
from http.client import HTTPException
from os import stat
from typing import Optional
from urllib.request import Request
from xmlrpc.client import boolean
from fastapi import Body, Cookie, FastAPI, Query, Path, Header, status, Form, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError

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

book_titles = {
    "The Lord of the Rings": "J. R. R. Tolkien",
    "Le Petit Prince": "Antoine de Saint-Exupéry",
    "Harry Potter and the Philosopher's Stone": "J. K. Rowling",
    "And Then There Were None": "Agatha Christie",
    "Dream of the Red Chamber": "Cao Xueqin",
}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oppps! {exc.name} did something wrong"}, 
        headers={"X-Error": "Wow, finally made my own error exception handler"}
    )

@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=exc.status_code)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to my API"}


@app.post("/login", status_code=status.HTTP_200_OK)
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


@app.get("/get_book/{title}", status_code=status.HTTP_200_OK)
def getBook(title: str):
    if title not in book_titles:
        raise UnicornException(name=title)
    return {"Author": book_titles.get(title)}