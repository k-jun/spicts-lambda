from utils.mosaic_art import Images
import cv2

MAIN_IMAGE_PATH = './images/main/metrock_2018.jpg'
PIESE_IMAGE_PATH = 'images/pieces'

mosaic_art = Images(PIESE_IMAGE_PATH, MAIN_IMAGE_PATH, 0.8, 0.8).create_mosaic()
cv2.imwrite("./mosiac_art.png", mosaic_art)