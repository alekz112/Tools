# -*- coding: utf-8-sig -*-

from __future__ import print_function
import re
import json
from pprint import pprint
from grab import Grab

from dictDe import *

def tranlsate(word, key, lan1='de', lan2='ru', alt=True, syn=True):
    """Prints the number of counts, word, translation, and example
    from lan1 to lan2 according to Translate.Google."""
    # First, write down a translation in some auxiliary txt file
    # and load it in json format
    g = Grab(log_file = 'dict.txt')
    link = 'http://translate.google.ru/translate_a/t?client=x&text='\
           + word + '&sl=' + lan1 + '&tl=' + lan2
    g.go(link)
    data = json.load(open('dict.txt'))
    # Then, let's try to get all the necessary elements in json
    translation, noun, alternatives, synonims = 0, 0, 0, 0
    try:
        translation = data[u'sentences'][0][u'trans']
        noun = data[u'dict'][0][u'pos']
        alternatives = data['dict'][0]['terms']
        synonims = data['dict'][0]['entry'][0]['reverse_translation']
    except:
        pass
    # German nouns should begin with capital letter
    if lan1=='de' and noun==u'имя существительное':
        word = word.title()
    # Finally, print out counts, word, translation with alternatives
    # and synonims, if applicable. Encoding is added up to allow
    # printing in cmd if you have a russian version of Windows
    if translation:
        print ('['+str(key)+']', word, ': ', translation)
        if alt and alternatives:
            [print (i, end=', ') for i in alternatives]
            print ('\r')
        if syn and synonims:
            [print (i.encode('cp866', errors='replace'), end=', ')
                                     for i in synonims]
            print ('\n')


def word_count_dict(filename, dictList=de50):
    """Returns a dictionary with key being number of counts
    and value being a list of words with that key.
    dictList is an optional argument: it is to eliminate
    the most common words. Default is the dictionary of
    the 50 most common German words"""
    
    count = {}
    txt = open(filename, 'r').read().lower()
    txt = re.sub('[,.!?":;()]', '', txt)
    words = txt.split()
    for word in words:
      if not word in count:
        count[word] = 1
      else:
        count[word] += 1
    return {i: sorted([w for w in count
               if (count[w]==i and w not in dictList.values())],
               key=lambda x: txt.index(x)) for i in set(count.values())}


def print_top(filename, n=10):
    """Generates the top count groups for the given file.
    Default number equals 10. Drop reverse if you want
    to print the less frequent words in the text."""
    
    mydict = word_count_dict(filename)
    mydict_keys = sorted(mydict, reverse=True)[0:n]
    [[tranlsate(word, key) for word in mydict[key]] for key in mydict_keys]
