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


parser = argparse.ArgumentParser(description='Train model for Markov\'s passwords.')
parser.add_argument(dest='dictFile', type=str,
        help='A dictionary file to model words on.')
parser.add_argument(dest='modelFile', type=str,
        help='a file to output the model to.')
parser.add_argument('-l', '--lookback', dest='lb', type=int, default=5,
        help='Lookback in Markov chain.')
args = parser.parse_args()


with open(args.dictFile) as f:
    s = f.read()
    words = s.split()

if len(words) == 0:
    print("No words in dictionary.")
    exit(0)

gen = Generator(args.lb)
gen.train(words)

print("Entropy Rate: {}".format(gen.entropyRate()))

with open(args.modelFile, 'wb') as f:
    msgpack.dump(gen.toRepr(), f)
