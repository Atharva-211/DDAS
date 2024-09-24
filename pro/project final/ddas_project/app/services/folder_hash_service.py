import hashlib
import os
import json
from typing import Dict, List, Union

# In-memory storage for folder file hashes and duplicates
folder_hashes_db: Dict[str, Dict[str, Union[str, List[str], int]]] = {}
folder_duplicates_db: Dict[str, Dict[str, Union[str, List[str], int]]] = {}

# Temporary JSON file to store hashes and duplicates
TEMP_JSON_FILE = 'temp.json'

def save_to_temp_file(data: dict):
    with open(TEMP_JSON_FILE, 'w') as temp_file:
        json.dump(data, temp_file, indent=4)

def load_from_temp_file() -> dict:
    if os.path.exists(TEMP_JSON_FILE):
        with open(TEMP_JSON_FILE, 'r') as temp_file:
            return json.load(temp_file)
    return {}

def hash_file(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    file_size = 0
    
    # Read the file in chunks to hash
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024):
            sha256_hash.update(chunk)
            file_size += len(chunk)
    
    return sha256_hash.hexdigest(), file_size

def process_folder(folder_path: str):
    folder_hashes_db.clear()
    folder_duplicates_db.clear()
    
    # Walk through folder and process each file
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1][1:].lower()  # Get file extension
            hash_hex, file_size = hash_file(file_path)
            
            # Check for duplicates by hash
            if hash_hex in folder_hashes_db:
                folder_duplicates_db[hash_hex] = {
                    'hash': hash_hex,
                    'filenames': folder_hashes_db[hash_hex]['filenames'] + [file],
                    'extension': file_extension,
                    'size': file_size,
                    'locations': folder_hashes_db[hash_hex]['locations'] + [file_path]
                }
            else:
                folder_hashes_db[hash_hex] = {
                    'filenames': [file],
                    'extension': file_extension,
                    'size': file_size,
                    'locations': [file_path]
                }
    
    # Save the results to the temp.json file
    save_to_temp_file({
        'hashes': folder_hashes_db,
        'duplicates': folder_duplicates_db
    })
    
    return {
        'hashes': folder_hashes_db,
        'duplicates': folder_duplicates_db
    }

def get_all_folder_files() -> Union[Dict[str, str], List[Dict[str, Union[str, List[str], int]]]]:
    if not folder_hashes_db:
        return {"message": "No hashes found in memory"}
    
    return [{"sha256_hash": hash_hex, "filenames": info['filenames'], "extension": info['extension'], "size": info['size'], "locations": info['locations']} 
            for hash_hex, info in folder_hashes_db.items()]

def get_folder_duplicate_files() -> Union[Dict[str, str], List[Dict[str, Union[str, List[str], int]]]]:
    if not folder_duplicates_db:
        return {"message": "No duplicates found"}
    
    return [{"sha256_hash": hash_hex, "filenames": info['filenames'], "extension": info['extension'], "size": info['size'], "locations": info['locations']}
            for hash_hex, info in folder_duplicates_db.items()]
