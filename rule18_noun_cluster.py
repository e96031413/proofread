import os
from color_print import *
from p_arser import nlp
from p_arser import sentencizer

principle = color_magenta('''Writing Principle 18:
Avoid noun clusters (many nouns one after another).
''')

example = color_cyan('''One noun cluster:
the pair correlation and alpha clustering studies
''')

def get_noun_cluster(sentence, parser=None, cluster_size=3):
    '''look for noun clusters, return the list
    of noun-cluster index'''
    parsed_ex = parser(sentence)
    noun_cluster = None
    for nc in parsed_ex.noun_chunks:
        # check whether there is noun cluster in each noun chunk
        num_nouns = 0
        for idx, token in enumerate(nc):
            if token.tag_ == 'NN':
                num_nouns += 1
        if num_nouns >= cluster_size:
            noun_cluster = nc
    return noun_cluster


def report_noun_clusters(file_path, cluster_size=3):
    '''report long subjects for all sentences in the paper'''
    sentences = sentencizer(file_path)
    suggestions = []
    for sentence in sentences:
        sug = get_noun_cluster(sentence.text, parser=nlp, cluster_size=cluster_size)
        if sug: suggestions.append(sug)

    if len(suggestions):
        print("Report noun clusters for ", color_cyan(file_path.split('/')[-1]))
        for sug in suggestions:
            print(sug)
            print(color_blue("******************************************************"))




if __name__ == '__main__':
    sentence = "condensed matter and quantum many-body theoretical physicist"
    print(get_noun_cluster(sentence, nlp, 2))
