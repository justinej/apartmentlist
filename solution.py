# Apartment List coding challenge
# https://gist.github.com/NWKMF/6589960bc4d6a7a22cd81feff3e0f67b
#
# Two words are "friends" if they are within 1 Levenshtein distance
# of each other. https://en.wikipedia.org/wiki/Levenshtein_distance
#
# This code takes in a list of words, and determines friendships between
# all words. Then it calculates the social group and prints out the size
# of the social group for the word "LISTY"

import string
import time

all_dicts = ["dictionary.txt",
             "half_dictionary.txt",
             "quarter_dictionary.txt",
             "eighth_dictionary.txt",
             "very_small_test_dictionary.txt"]

# Reads dictionary and returns contents
# Input: path to dictionary (string)
# Returns: words in file (list of strings)
def process_file(fname):
    words = []
    f = open(fname, "r")
    for line in f:
        words.append(line[:-1].lower())
    f.close()
    return words

# Calculates all possible friends of a word (Levenshtein
# distance of one from the word)
# Input: word (string)
# Returns: list of strings
def possible_friends(word):
    possibles = set() # Set to avoid repeats
    alphabet = string.ascii_lowercase

    for i in xrange(len(word)):
        # Remove a letter
        possibles.add(word[:i] + word[i+1:])
        for letter in alphabet:
            if word[i] != letter:
                # Substitute a letter
                possibles.add(word[:i] + letter + word[i+1:])
    for i in xrange(len(word)+1):
        for letter in alphabet:
            # Add a letter
            possibles.add(word[:i] + letter + word[i:])
    possibles = list(possibles)
    return possibles

# Input: list of strings
# Returns: a dictionary of immediate friendships between words.
#   keys are words (strings), values are lists of friends not
#   including itself (list of strings)
def find_friends(words):
    friends = dict( [ [word, []] for word in words])
    for i, word in enumerate(words):
        if (i+1)%10000 == 0:
            print "Matched {} out of {} friends so far".format(i, len(words))
        for possible_friend in possible_friends(word):
            if possible_friend in friends:
                friends[word].append(possible_friend)
    return friends

# Finds social network of word (number of distinct words that are
# connected by friendships to the word)
# Input: the word (string),
#   dictionary index with default "very_tiny_dictionary" (int)
# Returns: list of words in social network (list of strings)
def social_network(word, dictionary = 4):
    word = word.lower()
    words = process_file(all_dicts[dictionary])
    friends = find_friends(words) #dictionary of friendships
    assert word in friends, "Word must be in dictionary"

    # DFS on friends
    social_network = set()
    queue = [word]
    visited = set([word])
    while queue:
        current = queue.pop()
        social_network.add(current)
        children = friends[current]
        for child in children:
            if child not in visited:
                visited.add(child)
                queue.append(child)
    return list(social_network)


### Tests
assert "fist" in social_network("FIST")
assert "groundwoods" in social_network("groundwood", 3)
assert set(social_network("FIST")) == set(social_network("LISTY"))
assert len(social_network("FIST")) == 5
assert "litanies" not in social_network("LITANY")
