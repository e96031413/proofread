#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple grammar checker using the ginger online api
"""
import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from color_print import *

from ginger import check_grammar
from p_arser import sentencizer

principle = color_magenta('''Principle: correct grammar
1. Spell correctly.
2. The subject and verb must both be singular or plural.
''')

example = color_cyan('''
Incorrect: The group of students are complaining about grades.
Correct: The group of students is complaining about grades.
Reason: The main subject "group" is single. The main verb "are complaining" is plural.

Incorrect: The people is wearing formal attire.
Correct: The people are wearing formal attire.
Reason: The main subject "people" is plural. The main verb "is wearing," is singular.
''')

def has_latex(sentence):
    '''this function checks whether there are latex phrase.
    return true if:
    1. ':' is in the sentence
    2. '$', '\', '#', '{', '}' are in the sentence'''
    stop_marks = [':', '$', '\\', '#', '{', '}', '&', '/']
    for m in stop_marks:
        if m in sentence:
            return True
    return False

def check_grammars(fpath):
    print("Check grammar for ", color_cyan(fpath.split('/')[-1]))
    sentences = sentencizer(fpath)
    for sentence in sentences:
        if has_latex(sentence.text): continue
        check_grammar(sentence.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gramma check using Ginger API,\
            usage: python check_grammar.py fpath.txt')

    parser.add_argument('filenames', metavar='f', type=str, nargs='+',
                    help='one file or a list of files for analysis')

    args = parser.parse_args()

    for fpath in args.filenames:
        check_grammars(fpath)
