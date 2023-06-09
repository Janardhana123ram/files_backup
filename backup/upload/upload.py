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
    """Upload files to AWS S3/Google Cloud Storage

    Methods:
        __init__(self, args, log) -> None: Initializes a new instance of the Upload class with the given args and log
        create_aws_session(self) -> Bucket Object: Returns a AWS S3 bucket session
        create_gcs_session(self) -> Bucket Object: Returns a Google Cloud Storage bucket session
        load_to_s3(self, file, bucket) -> Boolean: Returns True if file upload succesfully else False
        load_to_gcs(self, file, bucket) -> Boolean: Returns True if file upload succesfully else False

    Usage:
        >>> upload = Upload(args, log)
        >>> bucket = upload.create_aws_session()
        >>> file = "test_file.jpg"
        >>> upload.load_to_s3(file, bucket)
        True
        >>> bucket = upload.create_gcs_session()
        >>> file = "test_doc.pdf"
        >>> upload.load_to_gcs(file, bucket)
        True
    """

    def __init__(self, args=None, log=None):
        """Initialize the input args and log object

        gcp_creds: Initialize the google cloud service json file
        """

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
            object_name = os.path.basename(_file)
            bucket.upload_file(_file, object_name)
            return True
        except Exception as error:
            self.log.error(msg=str(error))
            return False

    def load_to_gcs(self, _file, bucket):
        """Upload a file to an Google Cloud Storage Bucket

        :param _file: File to upload
        :return: True if file was uploaded, else False
        """

        try:
            object_name = os.path.basename(_file)
            # Name of the file on the GCS once uploaded
            blob = bucket.blob(object_name)
            blob.upload_from_filename(_file)
            return True
        except Exception as error:
            self.log.error(msg=str(error))
            return False

    def create_aws_session(self):
        """Create AWS session and select bucket

        return: bucket instance if bucket exists in the AWS S3 resource
        """

        try:
            session = boto3.Session(
                aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            )

            # Select AWS S3 resource
            s3 = session.resource("s3")
            # Select S3 bucket
            s3.meta.client.head_bucket(Bucket=os.environ["AWS_S3_BUCKET"])
            bucket = s3.Bucket(os.environ["AWS_S3_BUCKET"])
            return bucket
        except ClientError as error:
            self.log.error(msg=str(error))
            return False

    def create_gcs_session(self):
        """Create GSC session and select the bucket

        return: bucket instance if bucket exists in the GCS
        """

        try:
            # Authenticate Google Cloud Storage using the service account private key
            client = storage.Client.from_service_account_json(
                json_credentials_path=self.gcp_creds
            )
            return storage.Bucket(client, os.environ["GCP_BUCKET"])
        except Exception as error:
            self.log.error(msg=str(error))
            return False

    def run(self):
        aws_files, gcp_files = [], []
        # Get files from current and subdirectories
        for root, dirs, files in os.walk(self.args.input_dir):
            if not files:
                self.log.info("No valid files found")
                continue
            for file in files:
                file_type = file.split(".")[-1]
                if file_type in IMAGES_MEDIA:
                    aws_files.append(os.path.join(root, file))
                elif file_type in DOCS:
                    gcp_files.append(os.path.join(root, file))

        # Perform upload operation to AWS S3 bucket if files exists related IMAGES_MEDIA
        if aws_files:
            bucket = self.create_aws_session()
            for file in aws_files:
                self.load_to_s3(file, bucket)

        # Perform upload operation to GSC bucket if files exists related DOCS
        if gcp_files:
            bucket = self.create_gcs_session()
            for file in gcp_files:
                self.load_to_gcs(file, bucket)
