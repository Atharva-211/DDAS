from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.folder_hash_service import process_folder, get_folder_duplicate_files, get_all_folder_files
from app.services.supabase_folder import save_json_to_supabase



router = APIRouter()

# Define a Pydantic model for the request body
class FolderPath(BaseModel):
    folder_path: str

@router.post("/upload-folder")
def upload_folder(folder: FolderPath):  # Change the parameter to accept the model
    try:
        result = process_folder(folder.folder_path)  # Access the folder path from the model
        return {
            "message": "Folder processed successfully",
            "hashes": result['hashes'],
            "duplicates": result['duplicates']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing folder: {str(e)}")


@router.get("/folder/hashes")
def get_folder_hashes():
    try:
        return get_all_folder_files()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving folder hashes: {str(e)}")

@router.get("/folder/duplicates")
def get_folder_duplicates():
    try:
        return get_folder_duplicate_files()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving folder duplicates: {str(e)}")
