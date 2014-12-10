from textClassify import *
import cPickle as pickle


def textClassifyPrintFriendly(text, categoryDict):
	print text + " --> " + textClassify(text, categoryDict)

#TEXT CLASSIFY TEST SCRIPT
categoryDict = dict()
try:
	categoryDict['Collector'] = pickle.load(open('modified_Collectors.pkl', 'rb'))
except:	
	categoryDict['Collector'] = constructCollectorSet()

try:
	categoryDict['Countries'] = pickle.load(open('modified_Countries.pkl', 'rb'))
except:
	categoryDict['Countries'] = constructCountriesSet()

try:
	categoryDict['USCounties'] = pickle.load(open('modified_USCounties.pkl', 'rb'))
except:
	categoryDict['USCounties'] = constructUSCountiesSet()

try:
	categoryDict['Species'] = pickle.load(open('modified_Species.pkl', 'rb'))
except:
	categoryDict['Species'] = constructSpeciesSet()

try:
	categoryDict['Collection'] = pickle.load(open('modified_Collections.pkl', 'rb'))
except:
	collectionSet = set()
	collectionSet.add("uc berkeley")
	categoryDict['Collection'] = collectionSet


categoryDict['Date']= constructDateSet()







#textClassifyPrintFriendly('Alex Ho', categoryDict)
#textClassifyPrintFriendly('Canada', categoryDict)
#textClassifyPrintFriendly('Chemsek', categoryDict)
#textClassifyPrintFriendly('EMEC 719888', categoryDict)
#textClassifyPrintFriendly('VII-1/9-1988', categoryDict)
#textClassifyPrintFriendly('June 8, 1993', categoryDict)

txtC = TextClassifier(categoryDict)
for i in range(1000,1050):
	txtC.textClassifyImage('text_output/processed_'+str(i)+'.txt')
txtC.printResultsDict()
txtC.returnSets()
	
	




