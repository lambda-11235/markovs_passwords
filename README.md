
# Markov's Passwords

Markov's passwords is a program to generate random passwords composed of strings
of pronounceable made up words. It is based off of the XKCD comic
["Password Strength"](https://www.xkcd.com/936/), and the observation that
made-up words are even more resistant to dictionary attacks from the
Computerphile episode
["How to Choose a Password"](https://www.youtube.com/watch?v=3NjQ9b3pgIg).

## How It Works

I use a Markov chain of word frequencies based of off the $n$ characters before
them. The higher $n$ is the more recognizable a character is. $n$ is taken to be
as large as possible up to a limit.

The program thus needs a dictionary file as input, and could theoretically work
on multiple languages, provided that they are alphebetic and not logographic
(like Chinese). See `dict/`.

## Contributing

Contributions are welcome and can be made via pull requests. Low-hanging fruit
includes adding dictionaries for more languages. Ideally these dictionaries
should have the 1000-4000, depending on the language, most common words in the
language. This is to ensure that the produced words are still somewhat
recognizable, and aren't being perturbed by words native speakers might not use
often enough to recognize.
