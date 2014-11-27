import urllib
import re
import os

PATH = os.getcwd()
FILE_PATH = os.path.join(PATH, 'images.text')
OUTPUT_PATH =os.path.join(PATH,'output/')
jpg_re = r'http://essigdb.+.jpg.\)'
result=[]
with open(FILE_PATH, 'r') as f:
	for line in f:
		match = re.findall(jpg_re, line)
		if match!= []:
			result+=match


for i in range(0, len(result)):
	result[i] = result[i].replace("')","")

counter = 0
for url in result:
	url = url.replace(" ", "%20")
	f = open(OUTPUT_PATH+str(counter)+'.jpg','wb')
	f.write(urllib.urlopen(url).read())
	f.close()
	counter+=1