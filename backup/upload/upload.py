import logging
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
import os

IMAGES_MEDIA = (
    "jpg",
    "png",
    "svg",
    "webp",
    "mp3",
    "mp4",
    "mpeg4",
    "wmv",
    "3gp",
    "webm",
)
DOCS = ("doc", "docx", "csv", "pdf")


class Upload:
    DESC = "Upload files to AWS S3/Google Cloud Storage"

    def __init__(self, args, log):
        self.args = args
        self.log = log
        self.rel_path = os.path.dirname(os.path.realpath(__file__))
        self.gcp_creds = os.path.join(self.rel_path, "gcp_creds.json")

    def load_to_s3(self, _file, bucket):
        """Upload a file to an S3 bucket

        :param _file: File to upload
        :return: True if file was uploaded, else False
        """

        try:
            print("Uploading {_file} ...".format(_file=_file))
            object_name = os.path.basename(_file)
            bucket.upload_file(_file, object_name)
        except ClientError as error:
            logging.error(error)
            return False
        return True

    def load_to_gcs(self, _file, bucket):
        """Upload a file to an Google Cloud Storage Bucket

        :param _file: File to upload
        :return: True if file was uploaded, else False
        """

        try:
            print("Uploading {_file} ...".format(_file=_file))
            object_name = os.path.basename(_file)
            # Name of the file on the GCS once uploaded
            blob = bucket.blob(object_name)
            blob.upload_from_filename(_file)
        except Exception as error:
            logging.error(error)
            return False
        return True

    def run(self):
        aws_files = []
        gcp_files = []
        for root, dirs, files in os.walk(self.args.input_dir):
            for file in files:
                file_type = file.split(".")[-1]
                if file_type in IMAGES_MEDIA:
                    aws_files.append(os.path.join(root, file))
                elif file_type in DOCS:
                    gcp_files.append(os.path.join(root, file))
                else:
                    continue

        if aws_files:
            session = boto3.Session(
                aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            )

            # Select AWS S3 resource
            s3 = session.resource("s3")
            # Select S3 bucket
            bucket = s3.Bucket(os.environ["AWS_S3_BUCKET"])

            for file in aws_files:
                self.load_to_s3(file, bucket)

        if gcp_files:
            # Authenticate Google Cloud Storage using the service account private key
            client = storage.Client.from_service_account_json(
                json_credentials_path=self.gcp_creds
            )

            bucket = storage.Bucket(client, os.environ["GCP_BUCKET"])
            for file in gcp_files:
                self.load_to_gcs(file, bucket)
