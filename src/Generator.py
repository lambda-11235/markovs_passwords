
from HiddenMarkov import HiddenMarkov


class Generator:
    """
    Wrapper around the HiddenMarkov class that trains from dictionaries and
    generates words.
    """

    def __init__(self, words, nodes, iterations, verbose=False):
        """
        words: A set of words to train the HMM from.
        nodes: The number of nodes in the HMM.
        iterations: The number of iterations to train for.
        verbose: Print auxiliary information to stdout.
        """
        charCnt = 0
        self.charMap = {}

        samples = []
        for w in words:
            samp = []

            for c in w:
                c = c.lower()

                if c not in self.charMap:
                    self.charMap[c] = charCnt
                    charCnt += 1

                samp.append(self.charMap[c])

            samples.append(samp)

        self.hmm = HiddenMarkov(nodes, len(self.charMap))
        self.hmm.train(samples, iterations, verbose)

        self.charMap = dict([(v, k) for (k, v) in self.charMap.items()])

    def reseed(self):
        """
        Reseed random number generator from current time.
        """
        self.hmm.reseed()

    def generate(self, length):
        """
        Generate a word of length `length`.
        """
        return ''.join([self.charMap[n] for n in self.hmm.generate(length)])
