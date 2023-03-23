import os
import boto3
import pytest
from google.cloud import storage
from upload import Upload
import logging

logger = logging.getLogger("test logger")
upload = Upload(log=logger)

def test_load_to_s3():
    """Upload file to AWS S3 bucket with test file."""

    file_path = 'test_file.txt'

    # Upload the test file to S3
    bucket = upload.create_aws_session()
    status = upload.load_to_s3(file_path, bucket)

    assert status == True

def test_create_aws_session():
    """Check bucket exists in the S3 resource"""

    status = upload.create_aws_session()
    assert status.name == os.environ["AWS_S3_BUCKET"]

def test_load_to_s3_failure():
    """Failed to upload object to non-exists bucket"""

    file_path = "test_file.txt"

    os.environ["AWS_S3_BUCKET"] = "test"
    bucket = upload.create_aws_session()
    # Upload the test file to S3
    status = upload.load_to_s3(file_path, bucket)

    assert status == False

def test_load_to_gcs():
    """Upload file to Google Cloud Storage bucket with test file."""

    file_path = 'test_file.txt'
    client = storage.Client.from_service_account_json(json_credentials_path=upload.gcp_creds)
    bucket = storage.Bucket(client, os.environ["GCP_BUCKET"])
    status = upload.load_to_gcs(file_path, bucket)
    assert status == True

def test_load_to_gcs_failure():
    """Failed to upload object to non-exists bucket."""

    file_path = 'test_file.txt'
    client = storage.Client.from_service_account_json(json_credentials_path=upload.gcp_creds)
    bucket = storage.Bucket(client, "secumenmedia1")
    status = upload.load_to_gcs(file_path, bucket)
    assert status == False

def test_create_aws_session_failure():
    """Check bucket exists in the S3 resource."""

    os.environ["AWS_S3_BUCKET"] = "test"
    status = upload.create_aws_session()
    assert status == False

def test_create_gcs_session():
    """Check bucket exists in the Google Cloud Storage."""

    status = upload.create_gcs_session()
    assert status.name == os.environ["GCP_BUCKET"]

def test_create_gcs_session():
    """Check bucket existence with invalid bucket."""

    os.environ["GCP_BUCKET"] = "test"
    status = upload.create_gcs_session()
    assert status == False
