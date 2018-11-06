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
import argparse

from Generator import Generator


parser = argparse.ArgumentParser(description='Create pronounceable passwords.')
parser.add_argument(dest='dictFile', type=str,
        help='A dictionary file to model words on.')
parser.add_argument('-c', '--chars-per-word', dest='chars', type=int,
        default=6, help='Number of characters per word.')
parser.add_argument('-w', '--words', dest='words', type=int, default=4,
        help='Number of words in password.')
parser.add_argument('-p', '--passwords', dest='passwords', type=int, default=5,
        help='Number of passwords to output.')
parser.add_argument('-s', '--separator', dest='sep', type=str, default='_',
        help='Word separation character.')
parser.add_argument('-l', '--lookback', dest='lb', type=int, default=20,
        help='Lookback in Markov chain.')
args = parser.parse_args()


with open(args.dictFile) as f:
    s = f.read()
    words = s.split()

if len(words) == 0:
    print("No words in dictionary.")
    exit(0)

gens = []
for i in range(0, args.lb):
    gen = Generator(i)
    gen.train(words)
    gens.append(gen)

charSet = set()
for word in words:
    for ch in word:
        if ch.isalpha():
            charSet.add(ch)


for i in range(0, args.passwords):
    # Build password from frequencies.
    password = ""
    for j in range(0, args.words):
        word = ""

        for k in range(0, args.chars):
            ch = None
            idx = k % args.lb

            # Try various lookback amounts until we get a prediction.
            while ch is None and idx >= 0:
                ch = gens[idx].nextChar(word)
                idx -= 1

            if ch is None:
                ch = random.choice(list(charSet))

            word += ch.lower()

        password += word[:args.chars]

        if j < args.words - 1:
            password += args.sep

    print(password)
