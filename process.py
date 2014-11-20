import csv
from Levenshtein import *
from warnings import warn

#Dependencies:
#Levenshtein - for fast string edit distance calculation in C - https://pypi.python.org/pypi/python-Levenshtein/0.11.2

#To Do - High Level
#Cleanse all other columns of typos / inconsistencies
#Perform voting to generate consensus on each element
	#weight by accuracy and re-run
#Process images -> extract strings and compare them to vocabulary lists to see where to put which text where


#To Do - Low Level
#Idea? - May be better/worse in some cases - Replace .distance() < X with .ratio() > Y
#Progress bar/calculation?
#Isolate cases that don't match correction



def main():
	
	list_of_dicts = list() #list to store csv in memory, where each row is a dictionary



	keys = get_keys() #set up columns of data

	#Reads CSV file as a dictionary
	with open('calbug_short.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		for row in reader:
			list_of_dicts.append(row) #copy data into memory

	number_of_rows = len(list_of_dicts) #used to calculate progress (to be implemented)

	#Do some processing of data here
	process_country(list_of_dicts)
	process_collector(list_of_dicts)



	#Write processed data to disk
	write_csv(keys,list_of_dicts)


def process_country(list_of_dicts): #standardize notation for countries
	countries = get_countries()
	print countries
	for row in list_of_dicts:
		if row['Country'] == '' or row['Country'] == None:
				continue

		#manual correction
		if row['Country'].upper() == 'USA':
			row['Country'] = 'United States'
			continue

		if StringMatcher(None, "united states of america", row['Country'].lower()).distance() < 3:
			row['Country'] = 'United States'
			continue


		#automatic correction
		for country in countries:
			sm = StringMatcher(None, country.lower(), row['Country'].lower())
			distance = sm.distance()
			if distance < 3:
				row['Country'] = country
				continue

def process_collector(list_of_dicts):
	collectors = get_collectors()
	print collectors
	for row in list_of_dicts:
		for collector in collectors:
			if row['Collector'] == '' or row['Collector'] == None:
				continue



			#automatic correction
			sm = StringMatcher(None,collector.lower(),row['Collector'].lower())
			distance = sm.distance()
			if distance < 4:
				row['Collector'] = collector
				continue

def get_keys():
	with open('calbug_short.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		keys = reader.next().keys()
	return keys

def get_countries():
	list_of_countries = list()
	with open('countries.tsv','rb') as countries:
		for country in countries:
			#print country
			if country != '':
				list_of_countries.append(country.strip())
	return list_of_countries

def get_collectors():
	list_of_collectors = list()
	with open('collectors.tsv', 'rb') as collectors:
		for collector in collectors:
			if collector != '':
				list_of_collectors.append(collector.strip())
	return list_of_collectors

def write_csv(fieldnames, data):
	with open("processed_calbug.csv", 'wb') as out_file:
		writer = csv.DictWriter(out_file, delimiter=',', fieldnames = fieldnames)
		writer.writeheader()
		for row in data:
			writer.writerow(row)



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

if __name__ == "__main__":
	# sm = StringMatcher(None, 'United States', 'United States of America')
	# print sm.ratio()
	# sm = StringMatcher(None, 'United States', 'United States')
	# print sm.ratio()
	# sm = StringMatcher(None, 'United States', 'united states')
	# print sm.ratio()
	# sm = StringMatcher(None, 'United States', 'United States Minor Outlying Islands')
	# print sm.ratio()
	# sm = StringMatcher(None, 'Slovakia', 'Slovenia')
	# print sm.ratio()
	main()

