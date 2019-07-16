
import tensorflow as tf
import random


class HiddenMarkov:
    """
    Hidden Markov Model support class.
    """
    def __init__(self, nodes, outputs, seed=None):
        """
        nodes: The number of hidden nodes in the transition graph.
        outputs: The number of outputs.
        seed: A seed for the random number generator.
        """
        self.nodes = nodes
        self.outputs = outputs

        self.sess = tf.Session()
        self.randGen = random.Random()

        self.transitions = self.sess.run(tf.random.uniform((nodes, nodes), name='transition'))
        self.emissions   = self.sess.run(tf.random.uniform((nodes, outputs), name='emission'))
        #self.transitions[:,:] = 1/nodes
        #self.emissions[:,:] = 1/outputs

        self.state = 0


    def reseed(self):
        """
        Reseed random number generator.
        """
        self.randGen.seed()


    def train(self, samples, iterations, reportProgress=False):
        """
        Train the HMM of a set of samples.
        This method uses the Baum–Welch algorithm.

        samples: A list of samples with values in the range [0, self.outputs).
                 `samples[i][t]` is the output for sample `i` at time `t`.
        iterations: The number of iterations to run for.
        reportProgress: Prints progress out as a percentage.
        """
        tf.random.set_random_seed(self.randGen.randint(0, 1 << 31))

        cnt = 0
        total = iterations*(3*len(samples) + self.outputs)
        def progress():
            nonlocal cnt
            nonlocal reportProgress

            if reportProgress:
                print("\r{:.1f}%    ".format(cnt/total*100), end='')
            cnt += 1

        for _ in range(iterations):
            ys = []
            es = []

            for s in samples:
                progress()

                (y, e) = self.getYE(s)
                ys.append(y)
                es.append(e)

            # Update transitions
            esum = 0
            ysum = 0

            for sidx in range(len(samples)):
                progress()

                for t in range(len(samples[sidx]) - 1):
                    esum += es[sidx][t]
                    ysum += ys[sidx][t]

            # TODO: Double check if this division is correct.
            if ysum is not 0:
                self.transitions = self.sess.run(esum/ysum)

            # Update emissions
            ysum = 0
            for sidx in range(len(samples)):
                progress()

                for t in range(len(samples[sidx])):
                    ysum += ys[sidx][t]

            for v in range(self.outputs):
                progress()

                ysumCond = 0

                for sidx in range(len(samples)):
                    for t in range(len(samples[sidx])):
                        if samples[sidx][t] == v:
                            ysumCond += ys[sidx][t]

                # TODO: Double check if this division is correct.
                if ysum is not 0:
                    self.emissions[:, v] = self.sess.run(ysumCond/ysum)

        if reportProgress:
            print()

    def getYE(self, sample):
        """
        Compute gamma and epsilon for a specific sample.
        """
        a = self.forward(sample)
        b = self.backward(sample)

        y = []
        for t in range(len(sample)):
            val = a[t]*b[t]
            val /= tf.math.reduce_sum(val)
            y.append(val)

        e = []
        for t in range(len(sample) - 1):
            x = tf.expand_dims(self.emissions[:, sample[t + 1]], 0)
            val = tf.transpose(a[t]) @ self.transitions * (b[t+1] @ x)
            val /= tf.math.reduce_sum(val)
            e.append(val)

        return (y, e)

    def forward(self, sample):
        """
        Run the forward algorithm for a sample.
        """
        a = [tf.expand_dims(self.emissions[:, sample[0]], 1)]

        for t in range(1, len(sample)):
            x = tf.expand_dims(self.emissions[:, sample[t]], 1)
            a.append(x * (self.transitions @ a[-1]))

        return a

    def backward(self, sample):
        """
        Run the backward algorithm for a sample.
        """
        b = [tf.expand_dims(self.emissions[:, sample[-1]], 1)]

        for tpre in range(1, len(sample)):
            t = len(sample) - 1 - tpre
            x = tf.expand_dims(self.emissions[:, sample[t + 1]], 1)
            b.append(self.transitions @ (x * b[-1]))

        b.reverse()

        return b


    def generate(self, length):
        """
        Generate a output sequence of length `length`.
        """
        ret = []
        self.state = 0

        for _ in range(length):
            ret.append(self.emit())
            self.transNext()

        return ret

    def emit(self):
        """
        Select an output for the current state.
        """
        return self.randGen.choices(range(self.outputs), self.emissions[self.state,:])[0]

    def transNext(self):
        """
        Transition to the next state.
        """
        self.state = self.randGen.choices(range(self.nodes), self.transitions[self.state,:])[0]
