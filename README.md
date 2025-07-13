# AWS_ArcGIS_Lambda_ImageService - AWS Lambda ArcGIS Project
ArcGIS API for Python in AWS Lambda used to publish ArcGIS Image Service:

This project contains an AWS Lambda function that can be triggered when a new raster file is uploaded to an S3 bucket. It utilizes the ArcGIS API for Python to create a dynamic image service in ArcGIS Online.

## Project Structure

```
AWS_ArcGIS_lambda_ImageService
├── src
│   ├── app.py                # Main AWS Lambda function
│   ├── utils
│   │   └── arcgis_helper.py  # Helper functions for ArcGIS API
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd aws-lambda-arcgis
   ```

2. **Install dependencies**:
   Ensure you have Python and pip installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure AWS Lambda**:
   - Create a new Lambda function in the AWS Management Console.
   - Set the trigger to be an S3 event for object creation in the specified bucket.
   - Upload the contents of the `src` directory to the Lambda function.

4. **Set environment variables**:
   Configure any necessary environment variables in the Lambda function settings, such as ArcGIS Online credentials.

## Usage

Once the Lambda function is deployed and configured, it will automatically trigger whenever a new raster file is uploaded to the specified S3 bucket. The function will process the file and create a dynamic image service in ArcGIS Online.

## Additional Information

- Ensure that the IAM role associated with the Lambda function has the necessary permissions to access S3 and interact with the ArcGIS API.
- Make sure that in addition to the ArcGIS API for Python, the Azure-blob-Storage library is also installed. This is already part of the ArcGIS_API_AWS_Lambda Layer here in Github
- For more details on the ArcGIS API for Python, refer to the official documentation.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
