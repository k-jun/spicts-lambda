import os
from os import listdir
from os.path import isfile, join
import boto3

IMAGE_PATH = "https://s3-ap-northeast-1.amazonaws.com/kakomon-share/"

s3 = boto3.client('s3',
    aws_access_key_id='AKIAIUEONOTV7FWG6M2Q',
    aws_secret_access_key='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',
    region_name='ap-northeast-1'
)

def delete_files(path):
    folder = path
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    return None


def get_filenames(path):
    onlyfiles = []
    response = s3.list_objects(
       Bucket="kakomon-share",
       Prefix=path
    )
    for each in response["Contents"]:
        if not each['Key'].endswith(".DS_Store"):
            onlyfiles.append(IMAGE_PATH+each['Key'])
    return onlyfiles
