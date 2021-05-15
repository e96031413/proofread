import os
from color_print import *
from p_arser import nlp
from p_arser import sentencizer

principle = color_magenta('''Writing Principle 11:
Avoid interruptions between subject and verb
and between verb and object.
''')

example = color_cyan('''
Bad: We conclude, based on very simplified models of solar variability,
that soloar variability is insignificant.

Good: We conclude that soloar variability is insignificant
based on very simplified models of solar variability,

Good: Based on very simplified models of solar variability,
we conclude that soloar variability is insignificant.
''')

def get_dependence(sentence, dep=['ROOT'], parser=None):
    '''dependence analysis to find subjects, verb, objects'''
    parsed_ex = parser(sentence)
    for idx, token in enumerate(parsed_ex):
        if token.dep_ in dep:
            return idx, token, parsed_ex
    return None, None, parsed_ex


def report_subject_interruption(sentence, max_len=10):
    '''report the long subject for one sentence '''
    idx_s, subj, parsed_ex = get_dependence(sentence, ['nsubj', 'csubj'], nlp)
    idx_v, verb, parsed_ex = get_dependence(sentence, ['ROOT'], nlp)
    idx_o, obj, parsed_ex = get_dependence(sentence, ['obj'], nlp)

    if (idx_s is None or idx_v is None): return None
    interruption_distance = abs(idx_v - idx_s)
    if interruption_distance > max_len:
        n_coma = 0
        interrupt_start= None 
        interrupt_end = None 
        suggestion = []
        for ii, token in enumerate(parsed_ex):
            if token.text == ',': 
                n_coma += 1
                if interrupt_start == None:
                    interrupt_start = ii
                else:
                    interrupt_end = ii

        if interrupt_start is None or interrupt_end is None or \
                interrupt_start < idx_s or interrupt_end > idx_v:
            return ""

        for ii, token in enumerate(parsed_ex):
            if ii < interrupt_start:
                suggestion.append(token.text)
            elif ii < interrupt_end:
                suggestion.append(color_red(token.text))
            else:
                suggestion.append(token.text)

        return ' '.join(suggestion)


def report_interruptions(file_path, max_len=25):
    '''report long subjects for all sentences in the paper'''
    sentences = sentencizer(file_path)
    suggestions = []
    for sentence in sentences:
        sug = report_subject_interruption(sentence.text, max_len=max_len)
        if sug: suggestions.append(sug)

    if len(suggestions):
        print("Report interruptions for ", color_cyan(file_path.split('/')[-1]))
        for sug in suggestions:
            print(sug)
            print(color_blue("******************************************************"))



if __name__ == "__main__":
    exmp = "We conclude, based on very simplified models of solar variability, that soloar variability is insignificant."
    report_subject_interruption(exmp, max_len=5)

