import boto3
import os
import mimetypes
import json
from botocore.exceptions import ClientError

# Initialize S3 client
s3 = boto3.client('s3')

# Replace with your bucket name and the folder containing your website files
bucket_name = 'sheeraz-cloud-resume'
website_folder = '/Users/sheeraz/Desktop/workspace/python-workspace/cloud-resume'

def create_s3_bucket(bucket_name):
    """
    Create an S3 bucket if it doesn't exist.
    """
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
        )
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket {bucket_name} already exists.")
        else:
            print(f"Error creating bucket: {e}")

def upload_files_to_s3(bucket_name, website_folder):
    """
    Upload website files to the S3 bucket.
    """
    for root, dirs, files in os.walk(website_folder):
        for file in files:
            file_path = os.path.join(root, file)
            key = file_path[len(website_folder)+1:].replace("\\", "/")  # Fix for Windows paths
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            try:
                s3.upload_file(
                    file_path, 
                    bucket_name, 
                    key,
                    ExtraArgs={'ContentType': content_type}
                )
                print(f"Uploaded {file_path} to {key} in bucket {bucket_name}.")
            except ClientError as e:
                print(f"Error uploading {file}: {e}")

def enable_static_website_hosting(bucket_name):
    """
    Configure S3 bucket for static website hosting.
    """
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'}
    }
    
    try:
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration
        )
        print(f"Static website hosting enabled for {bucket_name}.")
    except ClientError as e:
        print(f"Error enabling website hosting: {e}")

def set_bucket_policy(bucket_name):
    """
    Set S3 bucket policy to allow public read access.
    """
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    try:
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print(f"Bucket policy set to allow public access for {bucket_name}.")
    except ClientError as e:
        print(f"Error setting bucket policy: {e}")

if __name__ == "__main__":
    # Step 1: Create S3 bucket
    create_s3_bucket(bucket_name)

    # Step 2: Upload website files
    upload_files_to_s3(bucket_name, website_folder)

    # Step 3: Enable static website hosting
    enable_static_website_hosting(bucket_name)

    # Step 4: Set bucket policy for public access
    set_bucket_policy(bucket_name)
