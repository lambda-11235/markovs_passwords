
import numpy as np
import random


class HiddenMarkov:
    def __init__(self, nodes, outputs):
        self.nodes = nodes
        self.outputs = outputs

        self.transitions = np.random.random((nodes, nodes))
        self.emissions   = np.random.random((nodes, outputs))
        self.pi          = np.random.random(nodes)

        self.transitions /= self.transitions.sum()
        self.emissions   /= self.emissions.sum()
        self.pi          /= self.pi.sum()

        self.randGen = random.Random()
        self.state = 0

    def train(self, samples, iterations):
        """
        Baum–Welch algorithm
        """
        s = samples[0]

        for _ in range(iterations):
            a = self.forward(s)
            b = self.backward(s)

            y = np.zeros((self.nodes, len(s)))
            e = np.zeros((self.nodes, self.nodes, len(s) - 1))

            for t in range(len(s)):
                for i in range(self.nodes):
                    y[i, t] = a[i, t]*b[i, t]

                if y[:, t].sum() > 0:
                    y[:, t] /= y[:, t].sum()

            for t in range(len(s) - 1):
                for i in range(self.nodes):
                    for j in range(self.nodes):
                        e[i,j,t] = a[i, t]*self.transitions[i,j]*b[j, t+1]*self.emissions[j, s[t + 1]]

                if e[:, :, t].sum() > 0:
                    e[:,:,t] /= e[:,:,t].sum()

            # Update transitions
            for i in range(self.nodes):
                for j in range(self.nodes):
                    esum = 0
                    ysum = 0

                    for t in range(len(s) - 1):
                        esum += e[i, j, t]
                        ysum += y[i, t]

                    if ysum > 0:
                        self.transitions[i,j] = esum/ysum

            # Update emissions
            for v in range(self.outputs):
                for i in range(self.nodes):
                    ysumCond = 0
                    ysum = 0

                    for t in range(len(s)):
                        if s[t] == v:
                            ysumCond += y[i, t]
                        ysum += y[i, t]

                    if ysum > 0:
                        self.emissions[i, v] = ysumCond/ysum

            # Update Pi
            self.pi = y[:,0].copy()

    def forward(self, sample):
        a = np.zeros((self.nodes, len(sample)))

        for i in range(self.nodes):
            a[i,0] = self.pi[i] * self.emissions[i, sample[0]]

        for t in range(1, len(sample)):
            for i in range(self.nodes):
                a[i, t] = self.emissions[i, sample[t]] * sum([a[j, t - 1] * self.transitions[i, j] for j in range(self.nodes)])

        return a

    def backward(self, sample):
        b = np.zeros((self.nodes, len(sample)))

        for i in range(self.nodes):
            b[i, -1] = self.pi[i] * self.emissions[i, sample[-1]]

        for tpre in range(1, len(sample)):
            t = len(sample) - 1 - tpre

            for i in range(self.nodes):
                b[i, t] = 0

                for j in range(self.nodes):
                    b[i, t] += b[j, t+1] * self.transitions[i,j] * self.transitions[j, sample[t + 1]]

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
