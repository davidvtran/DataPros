from Levenshtein import *


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



#The following StringMatcher code is from the Levenshtein API.

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




if __name__ == '__main__':
	main()