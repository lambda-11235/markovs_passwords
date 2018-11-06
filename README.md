
# Markov's Passwords

Markov's passwords is a program to generate random passwords composed of strings
of pronounceable made up words. It is based off of the XKCD comic
["Password Strength"](https://www.xkcd.com/936/), and the observation that
made-up words are even more resistant to dictionary attacks from the
Computerphile episode
["How to Choose a Password"](https://www.youtube.com/watch?v=3NjQ9b3pgIg).

## Usuage

First the model needs to be trained
```
> python3 train.py dict.txt dict.model -l 5
```

Then we can generate passwords using
```
> python3 markovs_passwords.py eng_37k.model
guessi_henedn_xychol_benone
ggiero_hlorag_terpol_jetter
xinemi_quitab_vernic_mialle
rapher_terpro_tedlyw_utioni
denbur_dthway_npliab_icketi
```

## How It Works

I use a Markov chain of word frequencies based of off the $n$ characters before
them. The higher $n$ is the more recognizable a character is. If $n$ is to large
the model may end up outputting longer words verbatim from the dictionary, as
they are the only matches that are that long. In general $n$ should be selected
to give the highest entropy rate (outputted by the training program).

The program thus needs a dictionary file as input, and could theoretically work
on multiple languages, provided that they are alphebetic and not logographic
(like Chinese). See `dict/`.

## Model File Format

Model files are encoded using the msgpack format. They correspond to the
flowing JSON format.
```
<model> := {"lookback" : <lookback>, "charSet" : <charSet>, "models" : <submodels>}
<charSet> := [<char>, ...]
<submodels> := [<submodel>, ...]
<submodel> := {"lookback" : <lookback>,
               "freqs" : {<char> : {<char> : <freq>, ...}, ...}
```

Here's and example for a model trained on "cat", "call", and "late", with a
lookback of 2.
```
{'lookback': 2,
 'charSet': ['e', 't', 'c', 'a', 'l'],
 'models': [{'lookback': 1,
   'freqs': {'c': {'a': 1.0},
    'a': {'t': 0.6666666666666666, 'l': 0.3333333333333333},
    'l': {'l': 0.5, 'a': 0.5},
    't': {'e': 1.0}}},
  {'lookback': 2,
   'freqs': {'ca': {'t': 0.5, 'l': 0.5},
    'al': {'l': 1.0},
    'la': {'t': 1.0},
    'at': {'e': 1.0}}}]}
```

## Contributing

Contributions are welcome and can be made via pull requests. Low-hanging fruit
includes adding dictionaries for more languages. Ideally these dictionaries
should have the 1000-4000, depending on the language, most common words in the
language. This is to ensure that the produced words are still somewhat
recognizable, and aren't being perturbed by words native speakers might not use
often enough to recognize.
