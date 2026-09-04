import os
from dotenv import load_dotenv
from fastapi import FastAPI
app = FastAPI()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
db_url = os.getenv("DB_URL")

@app.get("/")
def read_root():
    return {"message": "Hello World"}