#!/usr/bin/env python
# coding: utf-8

# In[8]:


##Database Configuration


#MongoDB

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["chat_database"]
chats_collection = db["chats"]

##Models

from pydantic import BaseModel
from typing import List, Optional

class Chat(BaseModel):
    user_id: str
    conversation_id: str
    messages: List[dict]  # Each message contains text, timestamp, etc.

class ChatSummary(BaseModel):
    conversation_id: str
    summary: str

class UserChatHistory(BaseModel):
    user_id: str
    page: int
    limit: int
        
##API Endpoints

from fastapi import APIRouter, HTTPException, Depends
from app.database import chats_collection
from app.services.summarizer import generate_summary
from bson import ObjectId

router = APIRouter()

# Store Chat Messages
@router.post("/chats")
async def store_chat(chat: dict):
    result = await chats_collection.insert_one(chat)
    return {"message": "Chat stored successfully", "id": str(result.inserted_id)}

# Retrieve Chat
@router.get("/chats/{conversation_id}")
async def retrieve_chat(conversation_id: str):
    chat = await chats_collection.find_one({"conversation_id": conversation_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

# Summarize Chat
@router.post("/chats/summarize")
async def summarize_chat(conversation_id: str):
    chat = await chats_collection.find_one({"conversation_id": conversation_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    summary = await generate_summary(chat["messages"])
    return {"conversation_id": conversation_id, "summary": summary}

# Delete Chat
@router.delete("/chats/{conversation_id}")
async def delete_chat(conversation_id: str):
    result = await chats_collection.delete_one({"conversation_id": conversation_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}


@router.get("/users/{user_id}/chats")
async def get_user_chats(user_id: str, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    chats = await chats_collection.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
    return chats

##LLM Integration

import openai

openai.api_key = "your_openai_api_key"

async def generate_summary(messages: list):
    conversation_text = " ".join([msg["text"] for msg in messages])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize the following conversation:\n{conversation_text}",
        max_tokens=150
    )
    return response["choices"][0]["text"]

##Main Application


from fastapi import FastAPI
from app.routers import chats, users

app = FastAPI()

# Include Routers
app.include_router(chats.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chat Summarization API"}

##Dockerfile

##FROM python:3.10-slim
WORKDIR /app
COPY
##RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

##requirements.txt

fastapi
uvicorn
motor
pymongo
httpx
openai

##Run Locally
##Install dependencies:


pip install -r requirements.txt
Start the application:


uvicorn app.main:app --reload
http://127.0.0.1:8000/docs for API documentation.

Deploy Using Docker
Build Docker image:


docker build -t fastapi-chat-api .
Run the container:


docker run -p 8000:8000 fastapi-chat-api


# In[ ]:





# In[ ]:




