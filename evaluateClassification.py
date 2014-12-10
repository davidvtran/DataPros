

def main():
	numCorrect = 0
	numTotal = 0
	x=0
	for i in range(1000,1371):
		try:
			classificationOutput = 'classification_output/' + str(i) + '.txt'
			mannuallyClassified = 'manually_classified_results/manually_classified_' + str(i) + '.txt'
			f = list(open(classificationOutput, 'r'))
			g = list(open(mannuallyClassified, 'r'))

			if len(f) != len(g):
				x+=1
				print "Mismatch of number of lines in file #" + str(i)

			for j in range(len(f)):
				try:
					fText = f[j].strip().lower()
					gText = g[j].strip().lower()
					if fText == gText:
						numCorrect +=1
					elif (fText == 'countries' or fText == 'uscounties') and gText == "location":
						numCorrect +=1
					elif (fText == 'catalog_id' and gText == 'catalogid'):
						numCorrect +=1
					else:
						print "mismatch in file #" + str(i)
						print "Predicted: " + gText
						print "Should be: " + fText
						print ''

					numTotal += 1
				except:
					continue

		except IOError:
			continue

	print "Number of mismatched files: " + str(x)
	print "Number of correct predictions: " + str(numCorrect)
	print "Total number of predictions: " + str(numTotal)
	print "Accuracy: " + str(1.0 * numCorrect / numTotal * 100) + '%'


if __name__ == '__main__':
	main()