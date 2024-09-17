import json
import tempfile
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://icifjmntjnnbkolhuetc.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljaWZqbW50am5uYmtvbGh1ZXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzkzODEsImV4cCI6MjA0MTkxNTM4MX0._51rIr3lJnagXCrz_3HnvULFZi2MYycL3IF0uLQAnqo"  # Replace with your Supabase API key

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase(file_path: str, bucket_name: str, file_name: str):
    try:
        # Remove the existing file if it exists
        try:
            delete_response = supabase.storage.from_(bucket_name).remove([file_name])
            if delete_response.status_code != 200:
                print(f"Error deleting existing file: {delete_response.text}")
        except Exception as e:
            print(f"An error occurred while deleting existing file: {e}")

        # Upload the new file to Supabase Storage
        with open(file_path, "rb") as file:
            upload_response = supabase.storage.from_(bucket_name).upload(file_name, file)
        
        # Print the entire response for debugging
        print("Upload Response:", upload_response)
        print("Upload Response Status:", upload_response.status_code)
        print("Upload Response Body:", upload_response.text)
        
        # Check if response is successful
        if upload_response.status_code == 200:
            print(f"File uploaded successfully as {file_name}.")
        else:
            print(f"Error uploading file: {upload_response.text}")

    except Exception as e:
        print(f"An error occurred while uploading to Supabase: {e}")

def upload_data_to_supabase(data: dict, file_name: str):
    try:
        # Log data for debugging
        print(f"Uploading data to Supabase: {data}")

        # Ensure data is a list
        if not isinstance(data, list):
            raise ValueError("Invalid data format: expected a list")

        # Create a temporary file with the data
        json_data = json.dumps(data, indent=4)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(json_data.encode('utf-8'))
            temp_file_path = temp_file.name

        # Upload the temporary file to Supabase Storage
        bucket_name = "FIRBuck"  # Replace with your bucket name
        upload_to_supabase(temp_file_path, bucket_name, file_name)

        # Clean up the temporary file
        os.remove(temp_file_path)

    except Exception as e:
        print(f"An error occurred while processing data: {str(e)}")

# Example usage
if __name__ == "__main__":
    example_found = [
        {"sha256_hash": "dummyhash1", "filenames": ["file1.txt"]}
    ]
    example_duplicates = [
        {"sha256_hash": "dummyhash1", "filenames": ["file1.txt"]}
    ]
    upload_data_to_supabase(example_found, "found_data.json")
    upload_data_to_supabase(example_duplicates, "duplicate_data.json")
