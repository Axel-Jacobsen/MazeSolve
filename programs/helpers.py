import time, sys

from PIL import Image

def cropBorder(image_file):
    """
    Crop the 1px by 1px white border around a maze

    Takes in an image file, returns original file or new file depending on save_org
    """

    height, width = image_file.size

    filename = 'cropped_' + image_file.filename

    cropPic = image_file.crop((1,1,width-1,height-1)).save(filename)

    return filename

def print_replace(obj, wait_time=None):
    """
       Print option that will overwrite previous print.
       obj is what is being printed, wait_time is the
       time to wait if we are printing individual objects in
       a memory structure
    """
    sys.stdout.write("\r" + obj)
    sys.stdout.flush()

    if wait_time:
        time.sleep(wait_time)
