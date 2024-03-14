# AWS S3 Bucket Storage Service

This project demonstrates a Python script for interacting with an AWS S3 bucket. It provides functionalities to upload files and directories, download files and directories, delete files, delete directories, and view the content of the S3 bucket.

## Project Scheme
![alt text](scheme.jpg)

## Prerequisites
- Python 3.x
- AWS CLI configured with appropriate permissions

## Installation
1. Clone this repository:
   ```
   git clone <repository-url>
   ```

2. Install required Python packages:
   ```
   pip install boto3
   ```

3. Configure AWS CLI with appropriate credentials.

## Usage
Run the script `main.py` and follow the prompts to perform various operations on the AWS S3 bucket.

```bash
python main.py
```

### Operations
- **Upload file**: Upload a single file to the S3 bucket.
- **Upload directory**: Upload the entire directory and its contents to the S3 bucket.
- **Show S3 content**: View the content of the S3 bucket.
- **Delete file/directory**: Delete a file, a directory, or all files and directories from the S3 bucket.

## Script Details
The script utilizes the `boto3` library to interact with AWS S3. It contains functions for uploading files, uploading directories, downloading files, downloading directories, deleting files, deleting directories, and viewing S3 content.
