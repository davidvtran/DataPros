from textClassify import *

def textClassifyPrintFriendly(text, categoryDict):
	print text + " --> " + textClassify(text, categoryDict)

#TEXT CLASSIFY TEST SCRIPT
categoryDict = dict()

categoryDict['Collector']= constructCollectorSet()
categoryDict['Countries']= constructCountriesSet()
categoryDict['USCounties']= constructUSCountiesSet()
categoryDict['Date']= constructDateSet()
collectionSet = set()
collectionSet.add("uc berkeley")
categoryDict['Collection']= collectionSet


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
	
	




