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

def textClassify(text):

	categoryList = list()
	collectSet = constructCollectorSet()
	countriesSet = constructCountriesSet()
	usCountiesSet = constructUSCountiesSet()
	
	categoryList.append(collectSet)
	categoryList.append(countriesSet)
	categoryList.append(usCountiesSet)
	
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
	threshold = 10
	if(minDist < 10):
		#There is a category for this text
		catIndex = categoryDistances.index(minDist)

		if(catIndex == 0):
			return (categoryList[catIndex], categoryWords[catIndex], 'Collectors')
		elif(catIndex == 1):
			return (categoryList[catIndex], categoryWords[catIndex], 'Countries')
		elif(catIndex == 2):
			return (categoryList[catIndex], categoryWords[catIndex],'US Counties')

	else:
		return None



#Test Script
text = 'Alex Ho'
result = textClassify(text)
print result[1]
print distance(text, result[1])
print result[2]
