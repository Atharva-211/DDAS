import os
import json
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://icifjmntjnnbkolhuetc.supabase.co"  # Replace with your Supabase URL
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljaWZqbW50am5uYmtvbGh1ZXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzkzODEsImV4cCI6MjA0MTkxNTM4MX0._51rIr3lJnagXCrz_3HnvULFZi2MYycL3IF0uLQAnqo"  # Replace with your Supabase API key
BUCKET_NAME = "FIRBuck"

# Create Supabase client
def create_supabase_client() -> Client:
    try:
        print("Creating Supabase client...")
        client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        print("Supabase client created successfully.")
        return client
    except Exception as e:
        print(f"Failed to create Supabase client: {str(e)}")
        raise e

# Upload file to Supabase storage bucket
def upload_to_supabase(client: Client, bucket: str, file_path: str, file_key: str):
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        with open(file_path, 'rb') as file_data:
            print(f"Uploading {file_key} to bucket {bucket}...")
            response = client.storage.from_(bucket).upload(file_key, file_data, {
                "upsert": True  # This will replace existing file
            })
            if response.get('error'):
                raise Exception(f"Error uploading {file_key}: {response['error']['message']}")
            else:
                print(f"Upload successful: {file_key}")
            return response
    except Exception as e:
        print(f"Error during file upload: {str(e)}")

# Save folder/hashes and folder/duplicates to Supabase
def save_json_to_supabase(client: Client, folder_data: dict):
    try:
        print("Saving folder hashes and duplicates to Supabase...")
        # Save hashes to /folder/hashes.json
        hashes_data = folder_data.get('hashes', {})
        hashes_json_path = 'folder_hashes.json'
        with open(hashes_json_path, 'w') as f:
            json.dump(hashes_data, f, indent=4)
        print(f"Hashes saved locally to {hashes_json_path}")
        upload_to_supabase(client, BUCKET_NAME, hashes_json_path, 'folder/hashes.json')

        # Save duplicates to /folder/duplicates.json
        duplicates_data = folder_data.get('duplicates', {})
        duplicates_json_path = 'folder_duplicates.json'
        with open(duplicates_json_path, 'w') as f:
            json.dump(duplicates_data, f, indent=4)
        print(f"Duplicates saved locally to {duplicates_json_path}")
        upload_to_supabase(client, BUCKET_NAME, duplicates_json_path, 'folder/duplicates.json')

        print("JSON data saved to Supabase successfully.")
    except Exception as e:
        print(f"Error saving JSON to Supabase: {str(e)}")

# Load data from temp.json
def load_temp_data() -> dict:
    try:
        if os.path.exists('temp.json'):
            print("Loading data from temp.json...")
            with open('temp.json', 'r') as temp_file:
                data = json.load(temp_file)
            print("Data loaded successfully.")
            return data
        else:
            print("No temp.json file found.")
            return {}
    except Exception as e:
        print(f"Error loading temp data: {str(e)}")
        return {}

# Main script
if __name__ == "__main__":
    try:
        # Initialize Supabase client
        supabase_client = create_supabase_client()

        # Load data from temp.json
        folder_data = load_temp_data()

        # Save the data to Supabase storage
        save_json_to_supabase(supabase_client, folder_data)

        print("Folder data uploaded to Supabase successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
