from process_images import *

def main():
	numCorrect = 0
	numTotal = 0
	x = 0

	for i in range(1000,5000):
		try:
			scriptOutput = 'text_output/processed_' + str(i) + '.txt'
			manuallyTranscribed = 'manually transcribed results/' + str(i) + '.txt'
			f = list(open(scriptOutput,'r'))
			g = list(open(manuallyTranscribed,'r'))

			
			if len(f) != len(g):
				x+=1
				print "Mismatch of number of lines in file #" + str(i)

			for i in range(len(f)):
				try:
					distance = StringMatcher(None,f[i],g[i]).distance()
					numCorrect += len(g[i]) - distance
					numTotal += len(g[i])
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