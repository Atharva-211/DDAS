from supabase import create_client, Client
from typing import List, Dict, Union, Set, Tuple

# Supabase credentials
SUPABASE_URL = "https://icifjmntjnnbkolhuetc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljaWZqbW50am5uYmtvbGh1ZXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzkzODEsImV4cCI6MjA0MTkxNTM4MX0._51rIr3lJnagXCrz_3HnvULFZi2MYycL3IF0uLQAnqo"

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_hash_exists(hash_hex: str) -> bool:
    try:
        response = supabase.table('other').select('hash').eq('hash', hash_hex).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking hash existence: {e}")
        return False

def upload_hashes_to_supabase(files: List[Dict[str, Union[str, List[str]]]]) -> Tuple[Set[str], Set[str]]:
    existing_hashes = set()
    new_hashes = set()
    try:
        for file_info in files:
            hash_hex = file_info['sha256_hash']
            
            # Check if the hash already exists in the database
            if check_hash_exists(hash_hex):
                print(f"Hash already exists in the database: {hash_hex}")
                existing_hashes.add(hash_hex)
                continue

            print(f"Attempting to insert hash: {hash_hex}")
            insert_response = supabase.table('other').insert({"hash": hash_hex}).execute()
            print("Insert Response:", insert_response)
            print("Insert Response Data:", insert_response.data)

            if insert_response.status_code == 201:
                print(f"Hash inserted successfully: {hash_hex}")
                new_hashes.add(hash_hex)
            else:
                print(f"Error inserting hash: {insert_response.data}")

    except Exception as e:
        print(f"An error occurred while inserting into Supabase table: {e}")
    
    return existing_hashes, new_hashes