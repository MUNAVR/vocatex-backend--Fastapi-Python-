from fastapi import FastAPI
from src.auth.routes import auth_router
from  contextlib import  asynccontextmanager
from src.db.main import init_db
from src.auth import utils
from fastapi.middleware.cors import CORSMiddleware
from src.jobs.routes import jobs_router
from src.job_seeker.routes import resume_router
from src.Job_applications.routes import apply_router

from fastapi import FastAPI, File, UploadFile, HTTPException
from src.messages.routes import messages_router
from src.messages.socket_server import sio, app as socket_app


@asynccontextmanager
async def  life_span(app:FastAPI):
    print(f"server is starting....")
    await init_db()
    yield
    print(f"server has been  stoped")

version="V1"

app=FastAPI(
    version=version,
    lifespan=life_span

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # List of origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=['auth'])
app.include_router(jobs_router,prefix=f"/api/{version}/jobs",tags=['jobs'])
app.include_router(resume_router,prefix=f"/api/{version}/resume",tags=['resume'])
app.include_router(apply_router,prefix=f"/api/{version}/apply_jobs",tags=['apply'])
app.include_router(messages_router,prefix=f"/api/{version}/messages",tags=['message'])

app.mount("/ws", socket_app) 



