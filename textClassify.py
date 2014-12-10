import csv
from Levenshtein import *
import cPickle as pickle
# try:
#    import cPickle as pickle
# except:
#    import pickle

def constructCollectorSet():
	collectorSet = set()
	with open('tsv_files/collectors.tsv', 'rb') as collectors:
		for collector in collectors:
			if collector != '':
				collectorSet.add(collector.strip().lower())
	return collectorSet

def constructCountriesSet():
	countrySet = set()
	with open('tsv_files/countries.tsv','rb') as countries:
		for country in countries:
			if country != '':
				countrySet.add(country.strip().lower())
	countrySet.add("mex.")
	return countrySet

def constructUSCountiesSet():
	countySet = set()
	with open('tsv_files/uscounties.tsv','rb') as countries:
		for country in countries:
			if country != '':
				countySet.add(country.strip().lower())
	return countySet

def constructDateSet():
	dateSet = set()
	with open('dates_and_romans.txt','r') as dates:
		for date in dates:
			dateSet.add(date.strip().lower())
	return dateSet

def constructSpeciesSet():
	speciesSet = set()
	with open('calbug.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		for row in reader:
			#list_of_dicts.append(row) #copy data into memory
			row = row['filename'].replace('.jpg','').strip().lower()
			row_parts = row.split(' ')
			i = 1
			specimenName = ''
			while i < len(row_parts):
				specimenName += row_parts[i] + ' '
				i+=1
			speciesSet.add(specimenName.strip().lower())
	#print speciesSet
	return speciesSet


	
class TextClassifier:

	def __init__(self, categoryDict):
		#categoryDict: 'Collector', 'Countries', 'USCounties', 'Date', 'Collection', 'Species'
		self.categoryDict = categoryDict
		self.resultsDict = dict()

	def cleanResultsDict(self):
		self.resultsDict = dict()

	def printResultsDict(self):
		for key in self.resultsDict.keys():
			print str(key) + ": " + str(self.resultsDict[key])

	def textClassifyImage(self, path):
		try:
			f = open(path, 'r')
			newDict = dict()
			for line in f:
				line = line.strip()
				category = self.textClassify(line)
				if category == 'Catalog_ID':
					line = line.replace(' ','')
				newList=list()
				if(category not in newDict):
					newList.append(line)
					newDict[category]=newList
				else:
					newDict[category].append(line)
			self.resultsDict[path]=newDict
		except IOError:
			return

	def textClassify(self, text):
		tempDict = self.categoryDict#.copy()

		#Classify Text into Name, Location, Collector, Collecting method, date, catalog_id
		
		#Remove useless EMEC
		text = text.strip().lower()
		if ('emec' in text): 	
			text = text.replace('emec','')
		
		
		#Extract information about text
		#Count Digits and Dashes in text
		digitCount=0;
		dashCount=0;
		for char in text:
			if(char.isdigit()):
				digitCount += 1
			elif(char == '-'):
				dashCount += 1

		#Check if text is Catalog ID
		if(digitCount > 5 and len(text) < 10 and dashCount == 0):
			return 'Catalog_ID' #+ ', Fixed Output: ' + text.replace(' ', '')

		#Check if text is a date
		if(digitCount > 1 and dashCount > 0):
			for date in tempDict['Date']:
				if date in text:
					return 'Date'

		categoryDistances = list()
		categoryWords = list()

		categoryAnalysisDict = dict()
		#del tempDict['Date']

		for key in tempDict.keys():
			targetSet = tempDict[key]
			closestWord = ""
			closestDistance = 100
			for word in targetSet:
				newDistance = min(closestDistance, distance(text, word))
				if(newDistance < closestDistance):
					closestWord = word
					closestDistance = newDistance
			categoryAnalysisDict[(key,closestWord)] = closestDistance 
		
		minDistKey = min(categoryAnalysisDict, key=categoryAnalysisDict.get)
		minDistVal = categoryAnalysisDict[minDistKey]

		#print 'Edit Distance: ' + str(minDistVal) + ' | Ratio: ' + str(ratio(minDistKey[1], text))
		if(minDistVal < 6) and ratio(minDistKey[1], text) > .5:
			#There is a category for this text
			return str(minDistKey[0]) #+ ' (Closest Word: ' + str(minDistKey[1]) + ')'

		else:
			return 'Nothing' #(Closest Word: ' + str(minDistKey[1]) + ')'

	def returnSets(self):
		for key in self.categoryDict:
			list_to_dump = self.categoryDict[key]
			if key == 'USCounties':
				pickle.dump(list_to_dump, open('modified_USCounties.pkl', 'a'))
			elif key == 'Countries':
				pickle.dump(list_to_dump, open('modified_Countries.pkl', 'a'))
			elif key == 'Collection':
				pickle.dump(list_to_dump, open('modified_Collections.pkl','a'))
			elif key == 'Collector':
				pickle.dump(list_to_dump, open('modified_Collectors.pkl', 'a'))
			elif key == 'Species':
				pickle.dump(list_to_dump, open('modified_Species.pkl', 'a'))







