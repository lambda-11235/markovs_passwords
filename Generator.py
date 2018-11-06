#!/usr/bin/python3

# Markov's passwords creates random pronounceable passwords using Markov chains.
# Copyright (C) 2018 Taran Lynn <taranlynn0@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import random


class LBGenerator:
    """
    A generator for a specific amount of lookback.
    """
    def __init__(self, lookback):
        self.lookback = lookback

        # Create a Markov chain that is represented as a map from prefixes of
        # lookback characters to character frequencies.
        self.freqs = {}


    def train(self, words):
        """
        Trains the model on a list of words.
        """
        for word in words:
            for i in range(0, len(word) - self.lookback):
                pre = word[i:(i + self.lookback)]
                post = word[i + self.lookback]

                if post.isalpha():
                    if pre not in self.freqs.keys():
                        self.freqs[pre] = {}

                    if post not in self.freqs[pre]:
                        self.freqs[pre][post] = 0

                    self.freqs[pre][post] += 1

        for pre in self.freqs.keys():
            fsum = sum(self.freqs[pre].values())

            if fsum > 0:
                for post in self.freqs[pre].keys():
                    self.freqs[pre][post] /= fsum


    def nextChar(self, word):
        """
        Predict what the next character in an unfinished word will be. Returns
        None if it can't get a prediction.
        """

        pre = self.freqs.get(word[-(self.lookback):])
        ch = None

        if pre is not None:
            keys = list(pre.keys())
            values = list(pre.values())
            # Randomly choose a character based off of its prefix characters and
            # its frequency.
            ch = random.choices(keys, values)[0]

        return ch


class Generator:
    """
    Generates new characters for words based off of a Markov chain.
    """
    def __init__(self, lookback):
        self.lookback = lookback

        # Create generators with varying amounts of lookback.
        self.gens = []
        for i in range(0, self.lookback):
            gen = LBGenerator(i + 1)
            self.gens.append(gen)

        self.charSet = set()


    def train(self, words):
        """
        Trains the model on a list of words.
        """
        for gen in self.gens:
            gen.train(words)

        self.charSet = set()
        for word in words:
            for ch in word:
                if ch.isalpha():
                    self.charSet.add(ch)


    def nextChar(self, word):
        """
        Predict what the next character in an unfinished word will be.
        """
        ch = None

        if self.lookback == 0:
            idx = -1
        else:
            idx = len(word) % self.lookback

        # Try various lookback amounts until we get a prediction.
        while ch is None and idx >= 0:
            ch = self.gens[idx].nextChar(word)
            idx -= 1

        if ch is None:
            ch = random.choice(list(self.charSet))

        return ch.lower()
