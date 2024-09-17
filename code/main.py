from fastapi import FastAPI, File, UploadFile
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

app = FastAPI()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"  # Use SQLite database URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a model for storing file hashes
class FileHash(Base):
    __tablename__ = "file_hashes"
    id = Column(String, primary_key=True, index=True)
    hash_value = Column(String, unique=True, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Helper function to compute SHA-256 hash of file content
def compute_sha256(file: UploadFile) -> str:
    sha256 = hashlib.sha256()
    for chunk in iter(lambda: file.file.read(4096), b""):
        sha256.update(chunk)
    file.file.seek(0)  # Reset file pointer to start
    return sha256.hexdigest()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Compute file hash
    file_hash = compute_sha256(file)
    
    # Save hash to the database
    db = SessionLocal()
    existing_file = db.query(FileHash).filter(FileHash.hash_value == file_hash).first()
    if existing_file:
        return {"result": "File with this content already exists"}
    
    new_file = FileHash(id=file.filename, hash_value=file_hash)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    
    return {"result": "File uploaded and hash stored"}

@app.post("/check")
async def check_files(file: UploadFile = File(...)):
    # Compute file hash
    file_hash = compute_sha256(file)
    
    # Check hash against stored values
    db = SessionLocal()
    existing_file = db.query(FileHash).filter(FileHash.hash_value == file_hash).first()
    if existing_file:
        return {"result": "File content matches an existing file"}
    else:
        return {"result": "File content does not match any existing files"}
