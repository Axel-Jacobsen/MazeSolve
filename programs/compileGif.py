# Python 3
# Create gif from image file

import moviepy.editor as mpy
import os

images = []
os.chdir('../mazes/creations/')
with open('name_file.txt', 'r') as namefile:

    for name in namefile:
        images.append(name.strip())

with open('name_file.txt', 'w') as namefile:
    namefile.write("")

images = ['file' + str(x) + '.png' for x in range(20001)]
# for i in range(100):
#     images.append('solution_olio.png')


fps = 10000
output_file = 'creation.gif'
clip = mpy.ImageSequenceClip(images, fps=fps)
clip.write_gif('{}'.format(output_file), fps=fps)

