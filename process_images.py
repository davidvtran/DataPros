# this requires installing Pillow, pytesseract
# Pillow - $sudo easy_install Pillow or install from http://pillow.readthedocs.org/en/latest/installation.html
# pytesseract - https://pypi.python.org/pypi/pytesseract

from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


original = Image.open("123.jpg") # open colour image
#image_file = original.convert('L') # convert image to black and white
# enhancer = ImageEnhance.Sharpness(original)

# enhancer.enhance(4).show()

sharpened = original.filter(ImageFilter.SHARPEN)

supersharpened = sharpened.filter(ImageFilter.SHARPEN)

for i in range(1):
	supersharpened = supersharpened.filter(ImageFilter.SHARPEN)


bw = supersharpened.convert('L')
greyscale = supersharpened.convert('1')



sharpened.save('sharpened.jpg')
supersharpened.save('supersharpened.jpg')
bw.save("black_and_white.jpg")
greyscale.save("greyscale.jpg")



print pytesseract.image_to_string(original)
print '-------------------------'
print pytesseract.image_to_string(sharpened)
print '-------------------------'
print pytesseract.image_to_string(supersharpened) 
print '-------------------------'
print pytesseract.image_to_string(supersharpened) 

