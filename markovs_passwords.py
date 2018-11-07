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


import argparse
import msgpack

from Generator import Generator


parser = argparse.ArgumentParser(description='Create pronounceable passwords.')
parser.add_argument(dest='modelFile', type=str,
        help='A file with the trained model.')
parser.add_argument('-c', '--chars-per-word', dest='chars', type=int,
        default=6, help='Number of characters per word.')
parser.add_argument('-w', '--words', dest='words', type=int, default=4,
        help='Number of words in password.')
parser.add_argument('-p', '--passwords', dest='passwords', type=int, default=5,
        help='Number of passwords to output.')
parser.add_argument('-s', '--separator', dest='sep', type=str, default='_',
        help='Word separation character.')
args = parser.parse_args()


with open(args.modelFile, 'rb') as f:
    rep = msgpack.load(f, raw=False)
    gen = Generator.fromRepr(rep)

print("Lookback: {}, Entropy Rate: {}".format(gen.lookback, gen.entropyRate()))
print("\nPasswords:")

for i in range(0, args.passwords):
    # Build password from frequencies.
    password = ""
    for j in range(0, args.words):
        word = ""

        for k in range(0, args.chars):
            word += gen.nextChar(word)

        password += word[:args.chars]

        if j < args.words - 1:
            password += args.sep

    print(password)
