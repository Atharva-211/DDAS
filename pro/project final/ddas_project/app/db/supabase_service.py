from supabase import create_client, Client
from typing import List

# Supabase credentials
SUPABASE_URL = "https://icifjmntjnnbkolhuetc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljaWZqbW50am5uYmtvbGh1ZXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzkzODEsImV4cCI6MjA0MTkxNTM4MX0._51rIr3lJnagXCrz_3HnvULFZi2MYycL3IF0uLQAnqo"  # Ensure to use a secure way to manage keys

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_table_name(file_extension: str) -> str:
    if file_extension.lower() == 'csv':
        return 'csv'
    elif file_extension.lower() == 'json':
        return 'json'
    else:
        return 'other'

def check_hash_exists(hash_hex: str, file_extension: str) -> bool:
    table_name = get_table_name(file_extension)
    try:
        response = supabase.table(table_name).select('hash').eq('hash', hash_hex).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking hash existence: {e}")
        return False

def upload_hash_to_supabase(hash_hex: str, file_name: str, file_size: int, file_extension: str, file_location: str) -> bool:
    table_name = get_table_name(file_extension)

    try:
        # Check if the file already exists
        existing_file = supabase.table(table_name).select('hash').eq('NAME', file_name).eq('LOCATION', file_location).execute()
        
        if len(existing_file.data) > 0:
            # Update the existing record
            response = supabase.table(table_name).update({
                "hash": hash_hex,
                "SIZE": file_size,
                "LOCATION": file_location
            }).eq('NAME', file_name).eq('LOCATION', file_location).execute()
            
            if response.error:
                raise Exception(f"Update failed: {response.error.message}")
            
            print("Update Response:", response)
        else:
            # Insert new record
            response = supabase.table(table_name).insert({
                "hash": hash_hex,
                "NAME": file_name,
                "SIZE": file_size,
                "LOCATION": file_location
            }).execute()
            
            if response.error:
                raise Exception(f"Insert failed: {response.error.message}")
            
            print("Insert Response:", response)
        
        if response.data:
            print(f"Hash processed successfully in {table_name} table: {hash_hex}")
            return True
        else:
            print(f"Error processing hash in {table_name} table: {response}")
            return False
    except Exception as e:
        print(f"An error occurred while processing the Supabase table: {e}")
        return False
