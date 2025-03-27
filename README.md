# Project Title: FastAPI Chat Summarization API

## Project Description
This FastAPI-based REST API processes user chat data efficiently. It supports real-time ingestion of chat messages, conversation retrieval and filtering, LLM-powered summarization, and heavy CRUD operations. Designed for scalability and performance, the project incorporates robust database indexing and async queries.

---

## Key Features
- **Store Chat Messages**: Save raw chat messages in the database.
- **Retrieve Chats**: Filter conversations by user, date, or keywords.
- **Summarize Chats**: Generate conversation summaries using an LLM.
- **Chat History**: Paginated retrieval for efficient handling of heavy load.
- **Delete Chat**: Securely delete conversations.

---

## Technologies Used
- **FastAPI**: Web framework for building the API.
- **Database**: MongoDB or PostgreSQL/MySQL (depending on your choice).
- **Async Programming**: Used for efficient query handling.
- **LLM Integration**: To summarize chat data.
- **Docker**: For containerized deployment.

---

## Installation
1.Set Up a Virtual Environment
Create and activate a Python virtual environment to isolate dependencies:

bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
2. Install Dependencies
Install the required Python libraries specified in the requirements.txt file:

bash
pip install -r requirements.txt
Dependencies include:

fastapi: For building the REST API.

uvicorn: ASGI server for running the app.

motor or sqlalchemy: For database operations (MongoDB or SQL).

httpx: To interact with external APIs.

openai: For LLM-based summarization.

3. Configure the Database
MongoDB:
Install MongoDB on your local machine or use a cloud-based service like MongoDB Atlas.

Configure the database connection in database.py:

python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['chat_database']

python
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "mysql+aiomysql://user:password@localhost/chat_db"
engine = create_async_engine(DATABASE_URL)

4. Set Up Environment Variables
Store sensitive information (e.g., API keys) in an .env file:

plaintext
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_url

5. Run the Application
Start the FastAPI application locally using Uvicorn:

bash
uvicorn app.main:app --reload
The API will be available at http://127.0.0.1:8000.

6. Test API Endpoints
Use tools like Postman or cURL to test the API. For example:

POST /chats: Store chat messages.

GET /chats/{conversation_id}: Retrieve chat details.

POST /chats/summarize: Summarize chat data using the LLM.

GET /users/{user_id}/chats?page=1&limit=10: Paginated chat history.

DELETE /chats/{conversation_id}: Delete chat messages.

7. Docker Deployment
To containerize the application for deployment:

Create a Dockerfile:

dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Build and run the Docker image:

bash
docker build -t fastapi-chat-api .
docker run -p 8000:8000 fastapi-chat-api
Usage and Deployment
API is accessible via endpoints described in the Test API Endpoints section.

Deployment on cloud services like AWS, Azure, or Heroku is also supported.

For local deployment, use Docker to containerize and run the application.

Contribution
Feel free to contribute to the project by creating pull requests or reporting issues.

License
This project is licensed under the MIT License

