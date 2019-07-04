
import numpy as np
import random


class HiddenMarkov:
    def __init__(self, nodes, outputs, seed=None):
        self.nodes = nodes
        self.outputs = outputs

        self.transitions = np.random.random((nodes, nodes))
        self.emissions   = np.random.random((nodes, outputs))

        #self.transitions[:,:] = 1/nodes
        #self.emissions[:,:] = 1/outputs

        self.randGen = random.Random()
        if seed is not None:
            self.randGen.seed(seed)

        self.state = 0


    # TODO
    # Optimize using matrix operations. Haven't done this yet because it's
    # tricky
    def train(self, samples, iterations):
        """
        Baum–Welch algorithm
        """
        np.random.seed(self.randGen.randint(0, 1 << 31))

        for _ in range(iterations):
            ys = []
            es = []

            for s in samples:
                (y, e) = self.getYE(s)
                ys.append(y)
                es.append(e)

            # Update transitions
            for i in range(self.nodes):
                for j in range(self.nodes):
                    esum = 0
                    ysum = 0

                    for sidx in range(len(samples)):
                        for t in range(len(samples[sidx]) - 1):
                            esum += es[sidx][t, i, j]
                            ysum += ys[sidx][t, i]

                    if ysum > 0:
                        self.transitions[i,j] = esum/ysum

            # Update emissions
            for v in range(self.outputs):
                for i in range(self.nodes):
                    ysumCond = 0
                    ysum = 0

                    for sidx in range(len(samples)):
                        for t in range(len(samples[sidx]) - 1):
                            if samples[sidx][t] == v:
                                ysumCond += ys[sidx][t, i]
                            ysum += ys[sidx][t, i]

                    if ysum > 0:
                        self.emissions[i, v] = ysumCond/ysum

            # Add some randomness so that we don't overfit.
            self.transitions += np.random.random(self.transitions.shape)/100
            self.transitions /= self.transitions.sum()

            self.emissions += np.random.random(self.emissions.shape)/100
            self.emissions /= self.emissions.sum()

    def getYE(self, sample):
            a = self.forward(sample)
            b = self.backward(sample)

            y = np.zeros((len(sample), self.nodes))
            e = np.zeros((len(sample) - 1, self.nodes, self.nodes))

            for t in range(len(sample)):
                for i in range(self.nodes):
                    y[t, i] = a[t, i]*b[t, i]

                if y[t, :].sum() > 0:
                    y[t, :] /= y[t, :].sum()

            for t in range(len(sample) - 1):
                for i in range(self.nodes):
                    for j in range(self.nodes):
                        e[t,i,j] = a[t, i]*self.transitions[i,j]*b[t+1, j]*self.emissions[j, sample[t + 1]]

                if e[t,:,:].sum() > 0:
                    e[t,:,:] /= e[t,:,:].sum()

            return (y, e)

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


    def generate(self, length):
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

    minChar = 255
    maxChar = 0

    with open('./dict/eng.txt') as f:
        samples = f.readlines()

    samples = random.sample(samples, 10)

    for i in range(len(samples)):
        samples[i] = [ord(c.lower()) for c in samples[i][:-1]]
        minChar = min(minChar, min(samples[i]))
        maxChar = max(maxChar, max(samples[i]))

    for i in range(len(samples)):
        samples[i] = [x - minChar for x in samples[i]]

    hmm = HiddenMarkov(100, maxChar - minChar + 1, seed=127)
    hmm.train(samples, 10)
    print(hmm.transitions)
    print(hmm.emissions)
    print(''.join(map(lambda n: chr(n + minChar), hmm.generate(30))))
