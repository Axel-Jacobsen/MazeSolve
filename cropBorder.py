"""
PURPOSE: To crop the 1px by 1px white border around a maze

PARAMS: Image file
RETURNS: Cropped Image Filename
"""
from PIL import Image

def cropBorder(image_file):

    height, width = image_file.size

    new_file_name = 'cropped' + image_file.filename

    cropPic = image_file.crop((1,1,width-1,height-1)).save(new_file_name)

    return new_file_name
