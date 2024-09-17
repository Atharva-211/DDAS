import json
import requests
import tempfile
from datetime import datetime
from supabase import create_client, Client

# Supabase credentials
url = "https://icifjmntjnnbkolhuetc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljaWZqbW50am5uYmtvbGh1ZXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzkzODEsImV4cCI6MjA0MTkxNTM4MX0._51rIr3lJnagXCrz_3HnvULFZi2MYycL3IF0uLQAnqo"

# Create Supabase client
supabase: Client = create_client(url, key)

# URL to fetch JSON data from
json_url = "http://127.0.0.1:8000/found"

# Fetch the JSON data
response = requests.get(json_url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse JSON data
data = response.json()

# Extract sha256_hash values
sha256_hashes = [item["sha256_hash"] for item in data]

# Convert the filtered data to JSON
filtered_data = {"sha256_hashes": sha256_hashes}
json_data = json.dumps(filtered_data)

# Create a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
    temp_file.write(json_data.encode('utf-8'))
    temp_file_path = temp_file.name

# Generate a unique file path in Supabase Storage
unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
file_path = f"sha256_hashes_{unique_suffix}.json"  # Append timestamp to ensure uniqueness

try:
    # Upload the temporary file to Supabase Storage
    bucket_name = "FIRBuck"  # Replace with your bucket name
    
    with open(temp_file_path, "rb") as file:
        upload_response = supabase.storage.from_(bucket_name).upload(file_path, file)

    # Print the entire response for debugging
    print("Upload Response:", upload_response)
    
    # Check if response is successful
    if upload_response.status_code == 200:
        print(f"File uploaded successfully as {file_path}.")
    else:
        print(f"Error uploading file: {upload_response.text}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up the temporary file
    import os
    os.remove(temp_file_path)
