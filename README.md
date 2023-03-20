# Backup
This tool is used to do files backup to the AWS S3 and Google Cloud Storage

Tools being used in this project
boto3 - https://pypi.org/project/boto3/
google-cloud-storage - https://pypi.org/project/google-cloud-storage/

## Requirements
- Python3
- pip3 (sudo apt install python3-pip)
- Python3 virtualenv (sudo pip3 install virtualenv)
- git CLI

## Setup
- Create python virtual environment (virtualenv -p python3 venv)
- Activate virtual environment (source vir/bin/activate)
- pip install -r requirements.txt
- AWS S3 creds
  - Generate ACCESS ID and SECRET KEY
  - Add to env variable
- Google Cloud Storage Service KEY
  - Generate service key and store it as JSON file
  - Copy JSON file to gcp_creds.json (files_backup/backup/upload/gcp_creds.json)
- Update ENV variables with valid inputs
  - Copy .env.example to .env
  - Read the comments in .env file an configure as necessary
  - Run `set -a && source .env && set +a`


## Tool usage
```
backup upload --help
usage: backup upload [-h] [--input-dir INPUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR
                        Media locations to upload

```

### Example command
```
backup upload --input-dir <dir_path>
```

### Run command
```
backup upload --input-dir /Users/janardhana/Downloads
```
