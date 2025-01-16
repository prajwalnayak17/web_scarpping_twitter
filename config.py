import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from mongo_db_service import MongoDBService

load_dotenv()

TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

app = FastAPI(
    description="""Twitter Scrapper is a web scrapping tool that logs into your personal Twitter account and scraped top 5 trending posts""",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration model
class TwitterCredentials(BaseModel):
    username: str = TWITTER_USERNAME
    password: str = TWITTER_PASSWORD

# Initialize MongoDB service
db_service = MongoDBService(MONGO_URI, DB_NAME, COLLECTION_NAME)

