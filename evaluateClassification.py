

def main():
	numCorrect = 0
	numTotal = 0
	x=0


	dateCorrect = 0
	speciesCorrect = 0
	locationCorrect = 0
	collectorCorrect = 0
	collectionCorrect = 0
	catalogIdCorrect = 0
	nothingCorrect = 0

	dateCount = 0
	speciesCount = 0
	locationCount = 0
	collectorCount = 0
	collectionCount = 0
	catalogIdCount = 0


	nothingCount = 0
	for i in range(1000,1371):
		try:
			classificationOutput = 'classification_output/' + str(i) + '.txt'
			mannuallyClassified = 'manually_classified_results/manually_classified_' + str(i) + '.txt'
			f = list(open(classificationOutput, 'r'))
			g = list(open(mannuallyClassified, 'r'))

			if len(f) != len(g):
				x+=1
				print "Mismatch in number of lines in file #" + str(i)

			for j in range(len(f)):
				try:
					fText = f[j].strip().lower()
					gText = g[j].strip().lower()

					if gText == 'date':
						dateCount +=1
					elif gText == 'species':
						speciesCount +=1
					elif gText == 'location':
						locationCount +=1
					elif gText == 'collector':
						collectorCount +=1
					elif gText == 'collection':
						collectionCount +=1
					elif gText == 'catalogid':
						catalogIdCount +=1
					elif gText == 'nothing':
						nothingCount +=1





					if fText == gText:
						numCorrect +=1
						if fText == 'date':
							dateCorrect +=1
						elif fText == 'species':
							speciesCorrect +=1
						elif fText == 'location':
							locationCorrect +=1
						elif fText == 'collector':
							collectorCorrect +=1
						elif fText == 'collection':
							collectionCorrect +=1
						elif fText == 'catalog_id':
							catalogIdCorrect +=1

					elif (fText == 'countries' or fText == 'uscounties') and gText == "location":
						numCorrect +=1
						locationCorrect +=1
					elif (fText == 'catalog_id' and gText == 'catalogid'):
						numCorrect +=1
						catalogIdCorrect +=1
					else:
						print "Prediction Error in file #" + str(i)
						print "Predicted: " + gText
						print "Should be: " + fText
						print ''

					if fText == 'nothing' and gText == 'nothing':
						nothingCorrect +=1

					numTotal += 1
				except:
					continue

		except IOError:
			continue

	print "Number of mismatched lines: " + str(x)
	print "Number of correct predictions: " + str(numCorrect)
	print "Total number of predictions: " + str(numTotal)
	print "Accuracy: " + str(1.0 * numCorrect / numTotal * 100) + '%'
	print ''

	print "Accuracy by category:"
	print "Date Accuracy: " + str(1.0 * dateCorrect / dateCount * 100) + '%'
	print "Species Accuracy: " + str(1.0 * speciesCorrect / speciesCount * 100) + '%'
	print "Location Accuracy: " + str(1.0 * locationCorrect / locationCount * 100) + '%'
	print "Collector Accuracy: " + str(1.0 * collectorCorrect / collectorCount * 100) + '%'
	print "Collection Accuracy: " + str(1.0 * collectionCorrect / collectionCount * 100) + '%'
	print "CatalogId Accuracy: " + str(1.0 * catalogIdCorrect / catalogIdCount * 100) + '%'
	print "Nothing Accuracy: " + str(1.0 * nothingCorrect / nothingCount * 100) + '%'

	#print "NothingCount: " + str(nothingCount)


if __name__ == '__main__':
	main()