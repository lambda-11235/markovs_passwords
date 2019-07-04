
import numpy as np
import random


class HiddenMarkov:
    def __init__(self, nodes, outputs):
        self.nodes = nodes
        self.outputs = outputs

        self.transitions = np.random.random((nodes, nodes))
        self.emissions   = np.random.random((nodes, outputs))

        #self.transitions[:,:] = 1/nodes
        #self.emissions[:,:] = 1/outputs

        self.randGen = random.Random()
        self.state = 0


    # TODO
    # 1. Change to handle multiple samples.
    # 2. Optimize using matrix operations. Haven't done this yet because it's
    #    tricky
    def train(self, samples, iterations):
        """
        Baum–Welch algorithm
        """
        s = samples[0]

        for _ in range(iterations):
            a = self.forward(s)
            b = self.backward(s)

            y = np.zeros((len(s), self.nodes))
            e = np.zeros((len(s) - 1, self.nodes, self.nodes))

            for t in range(len(s)):
                for i in range(self.nodes):
                    y[t, i] = a[t, i]*b[t, i]

                if y[t, :].sum() > 0:
                    y[t, :] /= y[t, :].sum()

            for t in range(len(s) - 1):
                for i in range(self.nodes):
                    for j in range(self.nodes):
                        e[t,i,j] = a[t, i]*self.transitions[i,j]*b[t+1, j]*self.emissions[j, s[t + 1]]

                if e[t,:,:].sum() > 0:
                    e[t,:,:] /= e[t,:,:].sum()

            # Update transitions
            for i in range(self.nodes):
                for j in range(self.nodes):
                    esum = 0
                    ysum = 0

                    for t in range(len(s) - 1):
                        esum += e[t, i, j]
                        ysum += y[t, i]

                    if ysum > 0:
                        self.transitions[i,j] = esum/ysum

            # Update emissions
            for v in range(self.outputs):
                for i in range(self.nodes):
                    ysumCond = 0
                    ysum = 0

                    for t in range(len(s)):
                        if s[t] == v:
                            ysumCond += y[t, i]
                        ysum += y[t, i]

                    if ysum > 0:
                        self.emissions[i, v] = ysumCond/ysum

            # Add some randomness so that we don't overfit.
            self.transitions += np.random.random(self.transitions.shape)/100
            self.transitions /= self.transitions.sum()

            self.emissions += np.random.random(self.emissions.shape)/100
            self.emissions /= self.emissions.sum()

    def forward(self, sample):
        a = np.zeros((len(sample), self.nodes))

        for i in range(self.nodes):
            a[0,i] = self.emissions[i, sample[0]]

        for t in range(1, len(sample)):
            for i in range(self.nodes):
                a[t, i] = self.emissions[i, sample[t]] * sum([a[t - 1, j] * self.transitions[i, j] for j in range(self.nodes)])

        return a

    def backward(self, sample):
        b = np.zeros((len(sample), self.nodes))

        for i in range(self.nodes):
            b[-1, i] = self.emissions[i, sample[-1]]

        for tpre in range(1, len(sample)):
            t = len(sample) - 1 - tpre

            for i in range(self.nodes):
                b[t, i] = 0

                for j in range(self.nodes):
                    b[t, i] += b[t+1, j] * self.transitions[i,j] * self.emissions[j, sample[t + 1]]

        return b


    def generate(self, length, seed=None):
        if seed is not None:
            self.randGen.seed(seed)

        ret = []
        self.state = 0

        for _ in range(length):
            ret.append(self.emit())
            self.transNext()

        return ret

    def emit(self):
        return self.randGen.choices(range(self.outputs), self.emissions[self.state,:])[0]

    def transNext(self):
        self.state = self.randGen.choices(range(self.nodes), self.transitions[self.state,:])[0]


if __name__ == '__main__':
    hmm = HiddenMarkov(100, 26)
    sample = list(map(lambda c: ord(c) - ord('a'), "bumblebee"))
    hmm.train([sample], 10)
    print(hmm.transitions)
    print(hmm.emissions)
    print(''.join(map(lambda n: chr(n + ord('a')), hmm.generate(30))))
