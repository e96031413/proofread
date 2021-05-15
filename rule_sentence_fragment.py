import os
from color_print import *
from parser import nlp
from parser import sentencizer

principle = '''Writing Principle from 
http://faculty.washington.edu/ezent/imsc.htm#FRAG

Avoid fragments in a sentence which are not complete, and therefore not grammatically correct.
E.g., (a) a missing subject (b) a missing verb (c) "danger" words not finished
'''

example = '''
The student felt nervous before the speech.
Thought about leaving the room.

The first is complete, because it contains both a subject and a verb. 
The second is not complete, because there is no subject.
'''

def sentence_fragment(sentence, parser=None):
    '''look for (a) a missing subject (b) a missing verb (c) "danger" words not finished'''
    parsed_ex = parser(sentence)
    # do dependency parsing to look for subject, verrb
    deps = [token.dep_ for token in parsed_ex]
    # don't check empty or very short sentences 
    if len(deps) < 3: return None

    subjs = ['nsubj', 'nsubjpass', 'csubj', 'csubjpass', 'expl']
    with_subj = False
    for subj in subjs:
        if subj in deps:
            with_subj = True
            break

    if not with_subj:
        return color_red("no subject: ") + sentence + '\n' + color_red(' '.join(deps))

    if not "ROOT" in deps:
        return color_red("no verb: ") + sentence + '\n' + color_red(' '.join(deps))

    return None


def report_sentence_fragments(file_path):
    '''report long subjects for all sentences in the paper'''
    sentences = sentencizer(file_path)
    suggestions = []
    for sentence in sentences:
        sug = sentence_fragment(sentence.text, parser=nlp)
        if sug: suggestions.append(sug)

    if len(suggestions):
        print("Report sentence fragments for", color_cyan(file_path.split('/')[-1]))
        for sug in suggestions:
            print(sug)
            print(color_blue("******************************************************"))




if __name__ == '__main__':
    sentence = "If you come home on time, I will buy you a present."
    print(sentence_fragment(sentence, nlp))
    report_sentence_fragments("tex/yilun.tex")
