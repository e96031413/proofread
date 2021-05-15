from texparser import parse_latex
import os

# to use this module, you have to install spacy and dict
dependence = ['pip install --user spacy', 'python -m spacy download en_core_web_sm']

nlp = None

try: 
    import spacy
    nlp = spacy.load('en_core_web_sm')
except:
    print("To use this module, you have to install spacy and dict. Start soon, ")
    for dep in dependence:
        os.system(dep)
    import spacy
    nlp = spacy.load('en_core_web_sm')

def set_custom_boundaries(doc):
    '''spacy does not set $. and }. as end of sentence.
    This custom boundary will fix that bug.  '''
    for token in doc[:-1]:
        if token.text == ";":
            doc[token.i+1].is_sent_start = True
        elif len(token.text) >= 2:
            if "$." == token.text[-2:] or "}." == token.text[-2:] \
                or "%." == token.text[-2]:
                doc[token.i+1].is_sent_start = True

        # do not use : as sentence end
        if token.text == ":" or token.text == "No." or token.text=="Nos.":
            doc[token.i+1].is_sent_start = False
    return doc


#add custom boundary once, skip if already exist
try:
    nlp.add_pipe(set_custom_boundaries, before="parser")
except:
    pass


def sentencizer(file_path):
    '''read file from file_path and sentencizer it,
    with custormized boundary $. and }.
    Return: doc.sents after parsed by nlp'''
    with open(file_path, "r", encoding='utf-8') as fsrc:
        src_text = fsrc.read()
    if '.tex' in file_path:
        src_text = parse_latex(src_text)
        src_text = ' '.join(src_text.split('\n'))
    doc = nlp(src_text)
    return doc.sents



if __name__ == '__main__':
    test_text = "This is a test for math $\delta\theta=\alpha\partial$, $, \alpha$. Does the customized sentencizer work?"
    i = 0
    for sen in nlp(test_text).sents:
        print(i, sen)
        i += 1

    #assert(len(list(nlp(test_text).sents)) == 2)
