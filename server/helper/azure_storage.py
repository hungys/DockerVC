import uuid
import base64
import config
from azure.storage.blob import BlobService

def upload_from_text(container, content):
    filename = str(uuid.uuid4())

    blob_service = BlobService(account_name=config.AZURE_STORAGE_NAME, account_key=config.AZURE_STORAGE_KEY)
    try:
        blob_service.put_block_blob_from_text(container, filename, content)
        return generate_blob_url(container, filename)
    except:
        return ""

def generate_blob_url(container, filename):
    return "https://%s.blob.core.windows.net/%s/%s" % (config.AZURE_STORAGE_NAME, container, filename)
