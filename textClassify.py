import csv
from Levenshtein import *

def constructCollectorSet():
	formal = set()
	with open('tsv_files/collectors.tsv', 'rb') as collectors:
		for collector in collectors:
			if collector != '':
				formal.add(collector.strip())
	return formal

def constructCountriesSet():
	formal = set()
	with open('tsv_files/countries.tsv','rb') as countries:
		for country in countries:
			if country != '':
				formal.add(country.strip())
	return formal

def constructUSCountiesSet():
	formal = set()
	with open('tsv_files/uscounties.tsv','rb') as countries:
		for country in countries:
			if country != '':
				formal.add(country.strip())
	return formal

def constructDateSet():
	dateSet = set()
	with open('dates_and_romans.txt','r') as dates:
		for date in dates:
			dateSet.add(date.strip())
	return dateSet

def textClassify(text):

	collectSet = constructCollectorSet()
	countriesSet = constructCountriesSet()
	usCountiesSet = constructUSCountiesSet()
	dateSet = constructDateSet()

	categoryList = list()
	categoryList.append(collectSet)
	categoryList.append(countriesSet)
	categoryList.append(usCountiesSet)

	#Classify Text into Name, Location, Collector, Collecting method, date, catalog_id
	
	#Remove useless EMEC
	text = text.strip()
	if ('EMEC' in text): 	
		text = text.replace('EMEC','')
	print "Check: " + text
	#Check if text is a catalog id
	digitCount=0;
	for char in text:
		if(char.isdigit()):
			digitCount += 1
	if(digitCount > 5 and len(text) < 10):
		return 'catalog_id'


	#Check if text is a date
	for date in dateSet:
		if date in text:
			return 'date'

	categoryDistances = list()
	categoryWords = list()

	for i in range(len(categoryList)):
		targetSet = categoryList[i]
		closestWord = ""
		closestDistance = 100
		for word in targetSet:
			newDistance = min(closestDistance, distance(text, word))
			if(newDistance < closestDistance):
				closestWord = word
				closestDistance = newDistance
		categoryDistances.append(closestDistance)
		categoryWords.append(closestWord)
	
	minDist = min(categoryDistances)
	
	print '-----------------'
	print closestWord
	print text
	print text + ': ' + str(ratio(closestWord,text))
	
	if ((minDist < 5) and (ratio(closestWord, text) > .7)):
		#There is a category for this text
		
		catIndex = categoryDistances.index(minDist)

		print(categoryWords[catIndex])
		
		if(catIndex == 0):
			return 'Collectors'
		elif(catIndex == 1):
			return 'Countries'
		elif(catIndex == 2):
			return 'US Counties'

	else:
		return 'Nothing'



#Test Script

f = open('text_output/processed_1007.txt', 'r')
for line in f:
	print line + ": " + textClassify(line)

"""
text = 'Alex Ho'
print text + ": " + textClassify(text)
print 'Canada' + ": " + textClassify('Canada')
print 'Chemsek' + ": " + textClassify('Chemsek')
print 'EMEC 719888' + ": " + textClassify('EMEC 719888')
print 'VII-1/9-1988' + ": " + textClassify('VII-1/9-1988')
print 'June 8, 1993' + ": " + textClassify('June 8, 1993')"""
