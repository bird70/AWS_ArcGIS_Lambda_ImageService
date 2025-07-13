from arcgis.gis import GIS
from arcgis.raster.analytics import copy_raster
import os
import logging
import tempfile
import boto3
import azure.storage.blob
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import BlobSasPermissions
from azure.storage.blob import BlobProperties
from azure.storage.blob import BlobLeaseClient

# Set the AWS_NO_SIGN_REQUEST environment variable
os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_dynamic_image_service(bucket, key):
    """
    Creates a dynamic image service in ArcGIS Online using the copy_raster function.

    Args:
        bucket (str): The name of the S3 bucket where the raster file is stored.
        key (str): The key (path) of the raster file in the S3 bucket.

    Returns:
        dict: Details of the created image service.
    """
    # # ArcGIS Online credentials (ensure these are set as environment variables for security)
    gis_url = os.getenv("ARCGIS_URL")
    username = os.getenv("ARCGIS_USERNAME")
    password = os.getenv("ARCGIS_PASSWORD")
    

    # Connect to ArcGIS Online
    gis = GIS(gis_url, username, password)

    # Extract the file extension from the S3 key
    file_extension = os.path.splitext(key)[1]  # Get the file extension (e.g., .tif, .jpg)

    # Download the raster file from S3
    s3 = boto3.client('s3')
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file_path = temp_file.name  # Save the file path with the correct extension
    # Close the file before downloading
    s3.download_file(bucket, key, temp_file_path)
    logger.info(f"Downloaded raster file from S3 to {temp_file_path}")

    # Define the output service name and properties
    key_name = key.split("/")[-1]  # Extract the file name from the key
    service_name = os.path.splitext(os.path.basename(key_name))[0]  # Use the file name (without extension) as the service name
    output_service = f"TEST8_WCRC_{service_name}_image_service"

    logger.info(f"Creating dynamic image service for raster: {key_name}")
    logger.info(f"Output service name: {output_service}")

    try:
        result = copy_raster(
            input_raster=temp_file_path,  # Use the local path for the raster file
            output_name=output_service,
            gis=gis,
            tiles_only=False,  # Ensure the service is dynamic
            raster_type_name="Raster Dataset",  # Specify the raster type
            context={ "extent": {
                "xmin": -180,
                "ymin": -90,
                "xmax": 180,
                "ymax": 90,
                "spatialReference": {"wkid": 4326}
            },
        }
        )
        logger.info(f"Dynamic image service created successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error during copy_raster: {str(e)}")
        raise
