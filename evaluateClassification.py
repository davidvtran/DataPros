def main():
	numCorrect = 0
	numTotal = 0
	x=0
	for in range(1000,5000):
		try:
			classificationOutput = ''
			mannuallyClassified = ''
			f = list(open(classificationOutput, 'r'))
			g = list(open(mannuallyClassified, 'r'))

			if len(f) != len(g):
				x+=1
				print "Mismatch of number of lines in file #" + str(i)

			for i in range(len(f)):
				try:
					if f[i] == g[i]:
						numCorrect +=1
					numTotal += 1
				except:
					continue

		except IOError:
			continue

print "Number of mismatched files: " + str(x)
print "Number of correct predictions: " + str(numCorrect)
print "Total number of characters: " + str(numTotal)
print "Accuracy: " + str(1.0 * numCorrect / numTotal * 100) + '%'


if __name__ == '__main__':
	main()