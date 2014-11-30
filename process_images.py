# this requires installing Pillow, pytesseract
# Pillow - $sudo easy_install Pillow or install from http://pillow.readthedocs.org/en/latest/installation.html
# pytesseract - https://pypi.python.org/pypi/pytesseract

from PIL import Image
import pytesseract



image_file = Image.open("123.jpg") # open colour image
image_file = image_file.convert('L') # convert image to black and white
image_file.save('result.jpg')


print pytesseract.image_to_string(Image.open('123.jpg'))
print '-------------------------'
print pytesseract.image_to_string(Image.open('result.jpg'))


