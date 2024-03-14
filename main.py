import boto3
import os

session = boto3.Session(profile_name='default')
s3 = session.client('s3')

bucket_name = "s3-bucket-storage-service"


def upload_file(file_path, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        response = s3.upload_file(file_path, bucket_name, object_name)
        print(f'File {file_path} uploaded to {bucket_name} as {object_name}')

    except Exception as e:
        print(
            f'Error uploading file {file_path} to {bucket_name} as {object_name}: {e}')
        return False


def upload_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.relpath(file_path, directory_path)
            s3_object_name = os.path.join(
                os.path.basename(directory_path), object_name)
            upload_file(file_path, s3_object_name)


def download_file(object_name, file_path):
    try:
        s3.download_file(bucket_name, object_name, file_path)
        print(f'File {object_name} downloaded from {bucket_name} to {file_path}')

    except Exception as e:
        print(
            f'Error downloading file {object_name} from {bucket_name} to {file_path}: {e}')
        return False


def download_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        response = s3.list_objects_v2(
            Bucket=bucket_name, Prefix=directory_path)
        for obj in response.get('Contents', []):
            file_path = os.path.join(
                directory_path, os.path.basename(obj['Key']))
            download_file(obj['Key'], file_path)
    except Exception as e:
        print(
            f'Error downloading directory {directory_path} from {bucket_name}: {e}')
        return False


def download_file(object_name, directory_path):
    try:
        file_name = input("Enter file name to download: ")
        file_path = os.path.join(directory_path, file_name) 
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        s3.download_file(bucket_name, object_name, file_path)
        print(f'File {object_name} downloaded from {bucket_name} to {file_path}')
    except Exception as e:
        print(f'Error downloading file {object_name} from {bucket_name} to {file_path}: {e}')
        return False


def delete_directory(directory_path):
    try:
        response = s3.list_objects_v2(
            Bucket=bucket_name, Prefix=directory_path)
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print(f'Directory {directory_path} deleted from {bucket_name}')
    except Exception as e:
        print(
            f'Error deleting directory {directory_path} from {bucket_name}: {e}')
        return False


def delete_all(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print(f'All files and directories deleted from {bucket_name}')
    except Exception as e:
        print(
            f'Error deleting all files and directories from {bucket_name}: {e}')
        return False


def show_s3_content():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        print(f'Content of {bucket_name} bucket:')
        for obj in response.get('Contents', []):
            print(f' - {obj["Key"]}')

        download_choice = input(
            "Enter 'd' to download a file/directory, 'r' to remove a file/directory, or any other key to exit: ")
        if download_choice.lower() == "d":
            object_name = input("Enter object name to download: ")
            file_path = input("Enter file path to download: ")
            download_file(object_name, file_path)
        elif download_choice.lower() == "r":
            delete_choice = input(
                "Enter 'f' to delete a file, 'd' to delete a directory, or '*' to delete all files and directories: ")
            if delete_choice == "*":
                delete_all(bucket_name)
            elif delete_choice.lower() == "f":
                object_name = input("Enter object name to delete: ")
                delete_file(object_name)
            elif delete_choice.lower() == "d":
                directory_path = input("Enter directory path to delete: ")
                delete_directory(directory_path)
            else:
                print("Invalid choice for deletion.")

    except Exception as e:
        print(f'Error showing content of {bucket_name} bucket: {e}')
        return False


if __name__ == "__main__":
    print("\n### Select option to perform operation in AWS S3 Bucket ###\n")
    print("---Upload file---           (u)")
    print("---Upload directory---      (ud)")
    print("---Show S3 content---       (v)")
    print("---Delete file/directory--- (r)")

    choice = input("Enter your choice: ")
    choice = choice.lower()

    if choice == "u":
        file_path = input("Enter file path to upload: ")
        upload_file(file_path)

    elif choice == "ud":
        directory_path = input("Enter directory path to upload: ")
        upload_directory(directory_path)

    elif choice == "v":
        show_s3_content()

    elif choice == "r":
        object_name = input("Enter object name to delete: ")
        delete_file(object_name)

    else:
        print("Invalid choice. Please enter valid choice.")
