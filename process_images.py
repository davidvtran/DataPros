# coding=utf-8
# this requires installing Pillow, pytesseract
# Pillow - $sudo easy_install Pillow or install from http://pillow.readthedocs.org/en/latest/installation.html
# pytesseract - https://pypi.python.org/pypi/pytesseract

from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import csv
from Levenshtein import *
from warnings import warn
import os
import time
import string
import re
import random

def setup_sharpened(input):
	sharpened = input.filter(ImageFilter.SHARPEN)
	sharpened = sharpened.filter(ImageFilter.SHARPEN)
	sharpened = sharpened.filter(ImageFilter.SHARPEN)
	sharpened.save('sharpened.jpg')
	return sharpened

def setup_supersharpened(input):
	supersharpened = input.filter(ImageFilter.SHARPEN)
	supersharpened = supersharpened.filter(ImageFilter.EDGE_ENHANCE)
	supersharpened = supersharpened.filter(ImageFilter.SHARPEN)
	supersharpened = supersharpened.filter(ImageFilter.SHARPEN)
	supersharpened.save('supersharpened.jpg')
	return supersharpened

def setup_bw(input):
	bw = input.convert('1')
	bw.save('black_and_white.jpg')
	bw = Image.open('black_and_white.jpg')
	bw = bw.filter(ImageFilter.EDGE_ENHANCE)
	bw.save('black_and_white.jpg')
	return bw

def setup_greyscale(input):
	greyscale = input.convert('L')
	greyscale.save('greyscale.jpg')
	greyscale = Image.open('greyscale.jpg')
	#greyscale = greyscale.filter(ImageFilter.SHARPEN)
	greyscale = greyscale.filter(ImageFilter.EDGE_ENHANCE)
	greyscale.save('greyscale.jpg')
	return greyscale


def process_all_transformations(original):
	sharpened = setup_sharpened(original)
	#supersharpened = setup_supersharpened(original)
	#bw = setup_bw(original)
	#greyscale = setup_greyscale(original)

	list_to_process = list()
	list_to_process.append((original, 'original'))
	#list_to_process.append((sharpened, 'sharpened'))
	#list_to_process.append((supersharpened, 'supersharpened'))
	#list_to_process.append((bw, 'black_and_white'))
	#list_to_process.append((greyscale, 'greyscale'))

	for pair in list_to_process:
		image = pair[0]
		name = pair[1]
		print name + ' output:'
		output =  pytesseract.image_to_string(image, 'eng', False, None).split('\n') #don't use config file
		#output =  pytesseract.image_to_string(image, 'eng', False, 'config.txt').split('\n') #use config file 
		processed_output = process_output(output)
		print '-----------------------------'
	return processed_output

def process_output(tesseract_output):
	#tesseract_output = os.linesep.join([s for s in tesseract_output.splitlines() if s])
	import string

	manual = construct_manual_vocab_list()
	post_processed = tesseract_output
	cleaned_data = list()
	i = 0

	#remove strangling characters
	for row in tesseract_output:
		lists = row.split(' ')
		cleaned_output = ''
		if row == '':
			continue
		for word in lists:
			word = filter(lambda x: x in string.printable, word)
			word = word.replace("'",'').replace('"','')
			word = word.replace('‘','')
			word = word.replace("»",'').replace('~','').replace('§','').replace('’','').replace('€','E').replace('«','').replace('¥','Y').replace('¢','e').replace('|','l')
			word = word.replace('}','')
			word = word.replace('_','')
			if len(word) < 2:
				pass
			else:
				cleaned_output += ' ' + word
		cleaned_data.append(cleaned_output.strip()) #re-stitch

	post_processed = cleaned_data

	for row in cleaned_data: #row is a string
		for string in manual:
			# if StringMatcher(None, string.lower(), row.lower()).distance() < 5:
			# 	post_processed[i] = string
			# 	continue
			if StringMatcher(None, string.lower(), row.lower()).ratio() > 0.65:
				post_processed[i] = string

			elif row !='' and row != None:
				pass
		i+=1

	# for row in post_processed:
	# 	print row
	return post_processed


def construct_master_set():
	formal = construct_formal_vocab_list()
	informal = construct_informal_vocab_list()
	manual = construct_manual_vocab_list()
	return formal.union(informal).union(manual) 

def construct_formal_vocab_list():
	formal = set()
	with open('collectors.tsv', 'rb') as collectors:
		for collector in collectors:
			if collector != '':
				formal.add(collector.strip())
	with open('countries.tsv','rb') as countries:
		for country in countries:
			if country != '':
				formal.add(country.strip())
	return formal



def construct_informal_vocab_list():
	informal = set()
	list_of_dicts = list() #list to store csv in memory, where each row is a dictionary

	with open('calbug.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		for row in reader:
			list_of_dicts.append(row) #copy data into memory
	for row in list_of_dicts:
		if row['Locality'] != '':
			informal.add(row['Locality'])
		if row['State/Province'] != '':
			informal.add(row['State/Province'])
	return informal



def construct_manual_vocab_list():
	manual = set()
	manual.add('UC Berkeley')
	manual.add('Berkeley')
	manual.add("EMEC")
	manual.add('Chemsak,at lites')
	manual.add('Biol.Los Tuxtlas')
	manual.add('Agrius')
	manual.add("Collector")
	manual.add("Powell")
	manual.add("at lites")
	manual.add("at light")
	return manual

def batch_process():
	for i in range(4000):
		i+=1006
		filename = 'archive/pic' + str(i) + '.jpg'
		print "Processing " + filename
		image = Image.open(filename)
		temp = process_all_transformations(image)
		temp = filter(None,temp)

		if is_good_output(temp):
			print temp
			f =  open('text_output/processed_' + str(i) + '.txt','w')
			for row in temp:
				f.write(row + '\n')
		

def is_good_output(output):
	warning_count = 0
	if len(output) < 4: 
		print "too short"
		return False
	#print output
	for line in output:
		# pattern = '(\W+)'
		# #m = re.compile(pattern)
		# m = re.match(line, pattern)
		# if m:
		# 	warning_count += len(m.groups())
		for character in line:
			if character not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ':
				warning_count+=1
	if warning_count > 6:
		print 'too many warnings'
		return False
	return True

def randomly_select_20_output():
	for i in range(6000):
		rand = random.random()
		if rand < 1/20:
			f =  open('text_output/processed_' + str(i) + '.txt','a')
			for line in f:
				print f






def main():
	start_time = time.time()
	#image = Image.open("archive/pic1008.jpg") # open colour image
	#process_all_transformations(image) 
	#batch_process()
	randomly_select_20_output()
	end_time = time.time()
	print "Processing took",end_time - start_time, 'seconds'




#The following StringMatcher code is from the Levenshtein API.

class StringMatcher:
    """A SequenceMatcher-like class built on the top of Levenshtein"""

    def _reset_cache(self):
        self._ratio = self._distance = None
        self._opcodes = self._editops = self._matching_blocks = None

    def __init__(self, isjunk=None, seq1='', seq2=''):
        if isjunk:
            warn("isjunk not NOT implemented, it will be ignored")
        self._str1, self._str2 = seq1, seq2
        self._reset_cache()

    def set_seqs(self, seq1, seq2):
        self._str1, self._str2 = seq1, seq2
        self._reset_cache()

    def set_seq1(self, seq1):
        self._str1 = seq1
        self._reset_cache()

    def set_seq2(self, seq2):
        self._str2 = seq2
        self._reset_cache()

    def get_opcodes(self):
        if not self._opcodes:
            if self._editops:
                self._opcodes = opcodes(self._editops, self._str1, self._str2)
            else:
                self._opcodes = opcodes(self._str1, self._str2)
        return self._opcodes

    def get_editops(self):
        if not self._editops:
            if self._opcodes:
                self._editops = editops(self._opcodes, self._str1, self._str2)
            else:
                self._editops = editops(self._str1, self._str2)
        return self._editops

    def get_matching_blocks(self):
        if not self._matching_blocks:
            self._matching_blocks = matching_blocks(self.get_opcodes(),
                                                    self._str1, self._str2)
        return self._matching_blocks

    def ratio(self):
        if not self._ratio:
            self._ratio = ratio(self._str1, self._str2)
        return self._ratio

    def quick_ratio(self):
        # This is usually quick enough :o)
        if not self._ratio:
            self._ratio = ratio(self._str1, self._str2)
        return self._ratio

    def real_quick_ratio(self):
        len1, len2 = len(self._str1), len(self._str2)
        return 2.0 * min(len1, len2) / (len1 + len2)

    def distance(self):
        if not self._distance:
            self._distance = distance(self._str1, self._str2)
        return self._distance

if __name__ == '__main__':
	main()

