from PIL import Image, ImageDraw, ImageFilter
from PIL.ImageChops import difference
import sys
import numpy as np
import cv2
import random
import requests
from io import BytesIO
import glob

import boto3

class Images:
    def __init__(self, piece_image_path, main_photo_path, alpha_piece_image, alpha_main_image):
        self.piece_image_path = piece_image_path
        self.main_image_path = main_photo_path

        # image_size = (height, width)
        self.image_size = (643, 643)
        self.alpha_piece_image = alpha_piece_image
        self.alpha_main_image = alpha_main_image
    
    def create_mosaic(self):
        # load main picture
        main_image = self.main_image_getter()

        # load piece pictures
        piece_image = self.piece_image_getter()

        # load mask picture
        mask_image = self.mask_getter(main_image.size).convert('1')

        # conbine these pictures
        mosaic_art = self.overlap(main_image, piece_image, mask_image)
        
        return mosaic_art


    def main_image_getter(self):
        response = requests.get(self.main_image_path)
        main_image = Image.open(BytesIO(response.content))
        # main_image = Image.open(self.main_image_path)
        # self.image_size = main_image.size
        return main_image

    def piece_image_getter(self):
        image_size = self.image_size
        images_list = self.piece_image_path
        random.shuffle(images_list)

        new_im = Image.new('RGB', (image_size[0]*7, image_size[1]*7))
        for i, elem in enumerate(images_list[:49]):
            print(i, elem)
            response = requests.get(elem)
            im = Image.open(BytesIO(response.content))
            
            image = im.resize(image_size)
            new_im.paste(image, (image_size[0]*(i%7), image_size[1]*(i//7)))
        return new_im

    def mask_getter(self, image_size):
        return Image.new("L", image_size, 128)

    def overlap(self, images, main_image, mask):
        images_resize = images.resize(self.image_size)
        main_image_resiz = main_image.resize(self.image_size)

        images_resize = images_resize.convert("RGB")
        main_image_resiz = main_image_resiz.convert("RGB")

        main_image = np.asarray(images_resize)
        images = np.asarray(main_image_resiz)

        dst = cv2.addWeighted(images, self.alpha_piece_image, main_image, self.alpha_main_image, 0)

        return dst
    
    
