import os
from color_print import *
from parser import nlp
from parser import sentencizer
from spacy.matcher import Matcher

principle = color_red('''Writing Principle 
Use active instead of passive sentence.
''')

example = color_green('''
:thumbdown: Cats are hated by dogs. \n
:thumbup: Dogs hate cats.
''')

passive_rule = [{'DEP':'nsubjpass'},{'DEP':'aux','OP':'*'},{'DEP':'auxpass'},{'TAG':'VBN'}]
matcher = Matcher(nlp.vocab)
matcher.add('Passive', None, passive_rule)

def check_passive(file_path):
    '''report all passive sentences in the paper'''
    sentences = sentencizer(file_path)
    text = '\n'.join([sentence.text for sentence in sentences])
    doc = nlp(text)
    matches = matcher(doc)

    if len(matches):
        print(color_blue("******************************************************"))
        print("Print passive sentences for", color_cyan(file_path.split('/')[-1]))
        for match in matches:
            start, end = match[1], match[2]
            print(doc[start:end])
        print(color_blue("******************************************************"))
