from fastapi import FastAPI
from app.routers import files, folder

app = FastAPI()

app.include_router(files.router)
app.include_router(folder.router)
