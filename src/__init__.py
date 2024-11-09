from fastapi import FastAPI, Depends,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from src.messages.routes import *
import json
from datetime import datetime

# Import routes and services
from src.auth.routes import auth_router
from src.db.main import init_db, get_session
from src.jobs.routes import jobs_router
from src.job_seeker.routes import resume_router
from src.Job_applications.routes import apply_router
from src.messages.routes import messages_router
from src.messages.service import ChatService
from src.messages.schemas import MessageCreate
from src.messages.connetct_manager import connection_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server has been stopped.")

app = FastAPI(
    version="V1",
    lifespan=lifespan
)

# Set up CORS middleware
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Include REST API routers
app.include_router(auth_router, prefix="/api/V1/auth", tags=['auth'])
app.include_router(jobs_router, prefix="/api/V1/jobs", tags=['jobs'])
app.include_router(resume_router, prefix="/api/V1/resume", tags=['resume'])
app.include_router(apply_router, prefix="/api/V1/apply_jobs", tags=['apply'])
app.include_router(messages_router, prefix="/api/V1/messages", tags=['message'])


def serialize_message(message_data):
    def convert_uuid_and_datetime(obj):
        if isinstance(obj, UUID):
            return str(obj)  # Convert UUID to string
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        raise TypeError(f"Type {type(obj)} not serializable")

    # Ensure all UUIDs and datetime objects in the data are converted to strings
    return json.loads(json.dumps(message_data, default=convert_uuid_and_datetime))

@app.websocket("/ws/chat/{user_id}")
async def chat_websocket_endpoint(websocket: WebSocket, user_id: str, session: AsyncSession = Depends(get_session)):
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message_data = MessageCreate(**data)

            # Save the message to the database
            saved_message = await chat_service.create_message(message_data, user_id, session)

            # Convert saved_message to JSON-serializable format
            serialized_message = serialize_message(saved_message.dict())

            # Send the message to both the intended recipient and the sender
            await connection_manager.broadcast(serialized_message)  # Send back to the sender

    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)


@app.websocket("/ws/webrtc/{user_id}")
async def webrtc_websocket_endpoint(websocket: WebSocket, user_id: str):
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "receiver_id" in data:
                await connection_manager.send_personal_message(data["receiver_id"], data)
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)
