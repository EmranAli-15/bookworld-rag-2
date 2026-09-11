import os
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import AsyncMongoClient
app = FastAPI()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
db_url = os.getenv("DB_URL")

mongo_client = AsyncMongoClient(db_url)
database = mongo_client.get_default_database()
books_collection = database["books"]

class Book(BaseModel):
    name: str
    image: str
    price: float
    rating: float
    summary: str
    quantity: int
    category: str
    writer: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book API!"}





@app.post("/add-book")
async def add_book(book: Book):
    book_dict = jsonable_encoder(book)
    result = await books_collection.insert_one(book_dict)
    return {"id": str(result.inserted_id)}


@app.get("/books/{mongodbId}")
async def read_book(mongodbId: str):
    try:
        book_id = ObjectId(mongodbId)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid MongoDB ID")

    book = await books_collection.find_one({"_id": book_id})

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return jsonable_encoder(book, custom_encoder={ObjectId: str})