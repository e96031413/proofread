import os
from color_print import *
from p_arser import nlp
from p_arser import sentencizer

principle = color_magenta('''Writing Principle 10
Get to the subject of the main sentence quickly,
and make it short and specific. if possible, use
central characters and topics as subjects.

This script looks for long subject and gives suggestion:
    Avoid long introductory phrases and long subjects!
''')

example = color_cyan('''
Bad: Due to the nonlinear and hence complex nature of ocean currents,
modeling these currents in the tropical pacific is difficult.

Good: Modeling ocean currents in the tropical Pacific is difficult 
due to their nonlinear and hence complex nature.
''')


# locate the subject of one sentence, report if there are many words before the subject
# or the subject is very long

def get_subject(sentence, parser=None):
    parsed_ex = parser(sentence)
    for idx, token in enumerate(parsed_ex):
        if token.dep_ == 'ROOT':
            return idx, token, parsed_ex
    return None, None, parsed_ex


def report_long_subject(sentence, max_len=10):
    '''report the long subject for one sentence '''
    idx, subj, parsed_ex = get_subject(sentence, nlp)
    if idx is None: return None
    if idx > max_len:
        long_phrase = []
        others = []
        for ii, token in enumerate(parsed_ex):
            #print(token, '--->', token.dep_)
            if ii < idx:
                long_phrase.append(token.text)
            else:
                others.append(token.text)
        suggestion = (color_red(' '.join(long_phrase))+' ') + (' '.join(others))
        return suggestion



def report_long_subjects(file_path, max_len=25):
    '''report long subjects for all sentences in the paper'''
    sentences = sentencizer(file_path)
    suggestions = []
    for sentence in sentences:
        sug = report_long_subject(sentence.text, max_len=max_len)
        if sug: suggestions.append(sug)

    if len(suggestions):
        print("Report long subjects for ", color_cyan(file_path.split('/')[-1]))
        for sug in suggestions:
            print(sug)
            print(color_blue("******************************************************"))


if __name__ == '__main__':
    example = "Due to the nonlinear and hence complex nature of ocean currents, modeling these currents in the tropical pacific is difficult."
    print(report_long_subject(example, max_len=10))
