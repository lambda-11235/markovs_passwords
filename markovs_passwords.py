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
parser.add_argument('-l', '--lookback', dest='lb', type=int, default=2,
        help='Lookback in Markov chain.')
args = parser.parse_args()


# Create a Markov chain that is represented as a map from prefixes of args.lb
# chars to character frequencies.
freqs = {}

with open(args.dictFile) as f:
    s = f.read()
    words = s.split()

for word in words:
    for i in range(0, len(word) - args.lb):
        pre = word[i:(i + args.lb)]
        post = word[i + args.lb]

        if pre not in freqs.keys():
            freqs[pre] = {}

        if post not in freqs[pre]:
            freqs[pre][post] = 0

        if post.isalpha():
            freqs[pre][post] += 1

for pre in freqs.keys():
    fsum = sum(freqs[pre].values())

    if fsum > 0:
        for post in freqs[pre].keys():
            freqs[pre][post] /= fsum


for i in range(0, args.passwords):
    # Build password from frequencies.
    password = ""
    for j in range(0, args.words):
        # TODO: Should we start with a word?
        word = random.choice(words)[:args.lb]
    
        for k in range(len(word), args.chars):
            pre = freqs.get(word[-(args.lb):])
    
            if pre is None:
                word += 'a'
            else:
                keys = list(pre.keys())
                values = list(pre.values())
                # Randomly choose a word based off of its prefix characters and its
                # frequency.
                word += random.choices(keys, values)[0]
    
        password += word[:args.chars]
    
        if j < args.words - 1:
            password += args.sep
    
    print(password)
