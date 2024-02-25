from PIL import Image
import os

CURRENTPATH = os.path.dirname(os.path.abspath(__file__))

imageName = "yagate_gs.png"

im = Image.open(f'{CURRENTPATH}\\image\\{imageName}')
im = im.convert('L')
im.save(f'{CURRENTPATH}\\image\\{imageName}')