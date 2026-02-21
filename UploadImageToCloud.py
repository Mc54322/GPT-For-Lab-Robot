from google.cloud import storage
import os

def upload_to_google_cloud(file_path):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # The path to your file to upload
    # The ID to give your GCS blob

    script_dir = os.path.dirname(__file__)
    key_file_path = os.path.join(script_dir, 'credentials.json')

    storage_client = storage.Client.from_service_account_json(key_file_path)
    bucket = storage_client.bucket('comc_gptapi_robot_images')
    blob = bucket.blob('current_image.jpg')

    blob.upload_from_filename(file_path)

    # Make the blob publicly viewable
    blob.make_public()

    #print(f"File {file_path} uploaded to current_image.jpg with public URL: {blob.public_url}")
    return blob.public_url