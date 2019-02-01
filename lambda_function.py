
from mosaic_art import Images
import cv2
import boto3
from PIL import Image
from io import BytesIO
import os
from random import randint

dynamodb = boto3.resource(
  'dynamodb',
  region_name='ap-northeast-1',
  aws_access_key_id=os.environ['DDBawsAccessKeyId'],
  aws_secret_access_key=os.environ['DDBawsSecretSccessKey']
)

s3 = boto3.resource(
  's3',
  region_name='ap-northeast-1',
  aws_access_key_id=os.environ['S3awsAccessKeyId'],
  aws_secret_access_key=os.environ['S3awsSecretSccessKey']
)

spictsBucket = s3.Bucket('spicts')
pieceImagesTable = dynamodb.Table('SpictsPieceImages')

MAIN_IMAGE_PATH = 'https://s3-ap-northeast-1.amazonaws.com/spicts/images.jpg'
PIESE_IMAGE_PATH = ['https://s3-ap-northeast-1.amazonaws.com/spicts/images.jpg', 'https://s3-ap-northeast-1.amazonaws.com/spicts/images.jpg']

def takeOut(x):
  return 'https://s3-ap-northeast-1.amazonaws.com/spicts/' + x['url']

def lambda_handler(event, context):
  PIESE_IMAGE_PATH = map(takeOut, pieceImagesTable.scan()['Items'])
  
  mosaic_art = Images(PIESE_IMAGE_PATH, MAIN_IMAGE_PATH, 0.8, 0.8).create_mosaic()
  img = Image.fromarray(mosaic_art, 'RGB')
  with BytesIO() as output:
    img.save(output, 'BMP')
    data = output.getvalue()
    spictsBucket.put_object(Key='mosaic_art/spictsMosaicArt' + str(randint(1, 5)) + '.png', Body=data)
  print("Done!")
  return 
  