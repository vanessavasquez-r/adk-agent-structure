

import os
import logging

import google.cloud.storage as storage
from google.api_core import exceptions

from app.app_utils.file_converter import pdf_to_txt, xlxs_to_txt, docx_to_txt, create_txt_file
from app.config import BUCKET_NAME, PROJECT_ID, LOCATION

def create_bucket_if_not_exists() -> None:
    """Creates a new bucket if it doesn't already exist.

    Args:
    """
    storage_client = storage.Client(project=PROJECT_ID)

    if BUCKET_NAME.startswith("gs://"):
        BUCKET_NAME = BUCKET_NAME[5:]
    try:
        storage_client.get_bucket(BUCKET_NAME)
        logging.info(f"Bucket {BUCKET_NAME} already exists")
    except exceptions.NotFound:
        bucket = storage_client.create_bucket(
            BUCKET_NAME,
            location=LOCATION,
            project=PROJECT_ID,
        )
        logging.info(f"Created bucket {BUCKET_NAME} in {LOCATION}")

def create_bucket_folder_if_not_exists(folder_name: str) -> None:
    """Creates a new bucket folder if it doesn't already exist.

    Args:
        folder_name: Name of the folder to create
    """
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)

    if not folder_name.endswith('/'):
            folder_name += '/'

    folder_name = folder_name.replace(" ", "")

    folder = bucket.blob(folder_name)
    if not folder.exists():
        folder.upload_from_string("")
        logging.info(f"Created folder {folder_name} in bucket {BUCKET_NAME}")
    else:
        logging.info(f"Folder {folder_name} already exists in bucket {BUCKET_NAME}")

def check_file_exists(folder_name: str, file_name: str) -> bool:
    """Checks if a file exists in a bucket.

    Args:
        folder_name: Name of the bucket folder to check
        file_name: Name of the file to check
    Returns:
        True if the file exists, False otherwise
    """
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        
        if not folder_name.endswith('/'):
            folder_name += '/'
        
        blob = bucket.blob(f"{folder_name}{file_name}")
        return blob.exists()
    except Exception as e:
        logging.error(f"Error checking file: {e}")
        return False

def upload_file_into_folder(folder_name: str, file_path: str) -> None:
    """Uploads a file into a bucket folder.

    Args:
        folder_name: Name of the folder to upload the file into
        file_path: Path to the file to upload
 
    """
    folder_name = folder_name.replace(" ", "")
    txt_file_name = "rfp_" + folder_name + ".txt"

    if check_file_exists(folder_name, txt_file_name):
        logging.info(f"File {txt_file_name} already exists in folder {folder_name}")
        return
    
    ext = file_path.split(".")[-1]

    content = ""
    if ext == "pdf":
        content = pdf_to_txt(file_path)
    elif ext == "xlsx":
        content = xlxs_to_txt(file_path)
    elif ext == "docx":
        content = docx_to_txt(file_path)
    else:
        logging.error(f"Unsupported file type: {ext}")
        return
    
    txt_file_path = create_txt_file(txt_file_name, content)

    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"{folder_name}/{txt_file_name}")
        blob.upload_from_filename(txt_file_path)
    except Exception as e:
        logging.error(f"Error uploading file: {e}")

def get_blob_from_gcs(folder_name: str, blob_name: str) -> None:
    """Gets a blob from a bucket.

    Args:
        folder_name: Name of the bucket folder to get the blob
        blob_name: Name of the blob to get
    Returns:
        The content of the blob as bytes
    """
    try:
        client = storage.Client(project=PROJECT_ID)

        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"{folder_name}/{blob_name}")

        logging.info(f"📥 Obteniendo archivo desde bucket: {BUCKET_NAME}, ruta: {blob_name}")
        content = blob.download_as_bytes()
        logging.info(f"✅ Archivo descargado correctamente ({len(content)} bytes).")
        return content
    except Exception as e:
        logging.error(f"Error getting blob: {e}")
        return None
    


    