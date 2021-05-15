import os
import re
from regex import Regex

def match_env_old_fasion(env='equation'):
    pattern = r'\\begin{\s*%s\s*\*?\s*}.*?\\end{\s*%s\s*\*?\s*}'%(env, env)
    return re.compile(pattern, re.I|re.M|re.S)

def match_begin_end_env(env='equation', get_content=True):
    '''matchs \begin{equation*} something ... \end{equation} 
    One special option is env='anything', will match all \begin{}*\end{}
    '''
    er = Regex()
    er.add(r"\\begin{")
    er.add(er.zero_or_more(er.whitespace()))
    if env == 'anything':
        env = er.non_greedy(er.zero_or_more(er.anything()))
    er.add(env)
    er.add(er.zero_or_more(er.whitespace()))
    er.add(er.zero_or_one(r'\*'))
    er.add(er.zero_or_more(er.whitespace()))
    er.add(r"}")
    if get_content: er.add(er.group_begin(name="content"))
    er.add(er.non_greedy(er.zero_or_more(er.anything())))
    if get_content: er.add(er.group_end())
    er.add(r"\\end{")
    er.add(er.zero_or_more(er.whitespace()))
    er.add(env)
    er.add(er.zero_or_more(er.whitespace()))
    er.add(er.zero_or_one(r'\*'))
    er.add(er.zero_or_more(er.whitespace()))
    er.add(r"}")
    er.compile()
    return er

def match_env(env='section', get_content=True):
    '''matchs text in the title or captions, \section{Chapter one}'''
    er = Regex()
    er.add(r"\\%s{"%env)
    if get_content: er.add(er.group_begin(name="content"))
    er.add(er.non_greedy(er.zero_or_more(er.anything())))
    if get_content: er.add(er.group_end())
    er.add(r"}")
    er.compile()
    return er

def remove_latex_comments(tex):
    '''remove the comment lines in latex src '''
    res = []
    for line in tex.split('\n'):
        if line.strip() == '': continue
        if line.strip()[0] == '%': continue
        res.append(line)
    return '\n'.join(res)


def remove_latex_backslash(tex):
    '''remove latex commands starting with \ such as
        \bibliographystyle{unsrt}
        \bibliography{inspire,not_inspire} 
    '''
    res = []
    for line in tex.split('\n'):
        if line.strip() == '': continue
        if line.strip()[0] == '\\': continue
        res.append(line)
    return '\n'.join(res)

def parse_latex(latex_src):
    '''1. get title, abstract, main body, acknowledgement
       2. remove equations, figures, tables from the tex
    '''
    tex = remove_latex_comments(latex_src)

    parts = []

    # get document
    m_doc = match_begin_end_env(env='document')

    try:
        tex  = m_doc.search(tex)[0]
    except:
        # the latex file can be split into many files
        # in which case many files do not have \begin{document}\end{document}
        tex = tex

    # get abstract if in \begin{}\end{} form
    try:
        m_abs = match_begin_end_env(env='abstract')
        abstract  = m_abs.search(tex)
        parts.append(abstract[0])
    except:
        pass

    # get abstract if in \abstract{}
    try:
        m_abs = match_env(env='abstract', get_content=True)
        abstract  = m_abs.search(tex)
        parts.append(abstract[0])
    except:
        pass


    try:
        m_captions = match_env(env='caption')
        captions = m_captions.search(tex)
        parts.extend(captions)

        sections = ['section', 'subsection', 'chapter', 'subsubsection']
        for section in sections:
            sec_titles = match_env(env=section, get_content=True)
            for sec_title in sec_titles.search(tex):
                sec_title = 'Title: ' + sec_title + '.'
                parts.append(sec_title)
    except:
        pass

    # remove anything that is inbetween \begin{} \end{} env
    # such as equations, eqnarray, tables, figures
    any_begin_end = match_begin_end_env(env="anything", get_content=False)
    tex = any_begin_end.sub('\n An equation, figure or something else is removed from the latex source file.', tex)

    tex = remove_latex_backslash(tex)

    parts.append(tex)

    return '\n'.join(parts)

    


if __name__ == '__main__':
    with open('tex/deformed.tex', 'r') as fin:
        tex = fin.read()
    res = parse_latex(tex)
    print(res)
