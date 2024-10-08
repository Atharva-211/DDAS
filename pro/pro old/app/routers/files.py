from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.hash_service import hash_and_store_file, get_all_files, get_duplicate_files
from app.supabase_service import upload_data_to_supabase

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = await hash_and_store_file(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/found")
def get_found_files():
    try:
        files = get_all_files()
        # Upload found files to Supabase
        upload_data_to_supabase(files, "found_data.json")
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving files: {str(e)}")

@router.get("/duplicate")
def get_duplicates():
    try:
        duplicates = get_duplicate_files()
        # Upload duplicates to Supabase
        upload_data_to_supabase(duplicates, "duplicate_data.json")
        return duplicates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving duplicates: {str(e)}")
