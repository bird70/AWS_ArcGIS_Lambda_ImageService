import json
import boto3
from utils.arcgis_helper import create_dynamic_image_service
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

''' 
Script used in an AWS lambda function for publishing a Dynamic Image Service in ArcGIS Online
You will need to have both the Azure storage Python library as well as the ArcGIS API for Python 
'''
def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            # Call the function to create a dynamic image service
            create_dynamic_image_service(bucket, key)
            return {
                'statusCode': 200,
                'body': json.dumps('Dynamic image service created successfully.')
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error creating dynamic image service: {str(e)}')
            }

# This enables local testing as a standalone script (not needed in Lambda)
if __name__ == "__main__":
    bucket = "arcgis-image-upload"
    key = "image/AY30_CopyRaster.tif"
    # Call the function to create a dynamic image service
    create_dynamic_image_service(bucket, key)
