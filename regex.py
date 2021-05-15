import re
#lgpang@qq.com
######################## regular expression for humman ############################

class Regex(object):
    '''It is painful that I forget python regular expression everytime for a while.
    So I construct this regular expression for human'''
    def __init__(self):
        self.pattern = r''
        self.engine = None
        self.is_compiled = False
        self.options = []

    def add(self, new_pattern=''):
        self.pattern += new_pattern

    def anything(self, include_newline=True):
        '''match anything using "."
        if option="with_newline", 
        self.options.append(re.S)
        '''
        if include_newline:
            self.options.append(re.S)
        return r'.'

    def whitespace(self):
        return r'\s'

    def non_greedy(self, inp):
        '''*?, +?, {m, n}? match as less as possible'''
        return inp + r'?'

    def non_whitespace(self):
        return r'\S'

    def zero_or_more(self, to_repeat=''):
        return r"%s*"%to_repeat

    def one_or_more(self, to_repeat=''):
        return r"%s+"%to_repeat

    def zero_or_one(self, to_repeat=''):
        return r"%s?"%to_repeat

    def repeat_m_to_n(self, to_repeat='', m=0, n=0):
        return r"%s{%s, %s}"%(to_repeat, m, n)

    def group_begin(self, name=''):
        '''start a group with name '''
        if name == '':
            return r"("
        else:
            return r"(?P<%s>"%name

    def group_end(self):
        '''close a group'''
        return r")"

    def compile(self, ignore_case=True, multi_line=True, dot_match_anything=True):
        options = re.VERBOSE
        if ignore_case: options = options | re.I
        if multi_line: options = options | re.M
        if dot_match_anything: options = options | re.S

        if len(self.options):
            for option in self.options:
                options = options | option

        self.engine = re.compile(self.pattern, options)
        self.is_compiled = True

    def search(self, input_str):
        if not self.is_compiled: 
            self.engine = re.compile(self.pattern, options)
            self.is_compiled = True
        results = self.engine.findall(input_str)
        return results

    def sub(self, to_str, src):
        '''substitute pattern to to_str in the src'''
        if not self.is_compiled: 
            self.engine = re.compile(self.pattern, options)
            self.is_compiled = True
        return self.engine.sub(to_str, src)

    def split(self, src):
        '''split src using the patterns as sep'''
        if not self.is_compiled: 
            self.engine = re.compile(self.pattern, options)
            self.is_compiled = True
        return self.engine.split(src)




######################## remind python re ###############################

def re_character_class(sets):
    '''equals to [], e.g., [abc] or [a-z]'''
    pass

def re_metacharacter(sets):
    '''metacharacters 
    . ^ $ * + ? { } [ ] \ | ( ) 
    who can not match themselves but has special meaning.
    When a metacharacter is used inside a class, it matchs itself,
    e.g., [akm$] matchs a, k, m and $.
    But ^ inside [] has special meaning -- complementing,
    e.g., [^5] matchs any character except 5. '''
    pass

def re_backslash():
    ''' \ escape all the metacharacters. E.g., if you want to match \ and [,
    you can precede them with a \ to remove their special meaning: \\ or \[.

    \w    matches any alphanumeric character,       [a-zA-Z0-9_]
    \W    matches any non-alphanumeric character,   [^a-zA-Z0-9_]
    \d    matches any digit character,              [0-9]
    \D    matches any non-digit character,          [^0-9]
    \s    matches any whitespace character,         [ \t\n\r\f\v]
    \S    matches any non-whitespace character,     [^ \t\n\r\f\v]
    '''
    pass

def re_anything():
    '''The final metacharacter is dot ".". 
    It matches anything except a newline character.
    In re.DOTALL mode it will match even a newline.
    It is used where you want to match "any character".
    '''
    pass

def re_repeat_zero_or_more():
    ''' * specifieds that the previous character can be matched zero or more times.
    It is greedy to repeat as many times as possible. '''
    pass

def re_repeat_one_or_more():
    ''' + specifieds that the previous character can be matched one or more times.
    It is greedy to repeat as many times as possible.
    '''
    pass

def re_repeat_zero_or_one():
    ''' ? specifieds that the previous character can be matched zero or one times.
    Make something optionional. e.g., home-?brew matchs either "homebrew" or "home-brew".
    '''
    pass

def re_repeat_m_to_n():
    '''{m, n} repeat the previous character at least m, at most n times.
    {0,} is the same as *, {1,} is the same as + and {0,1} is the same as ?'''
    pass

def re_non_greedy():
    '''non-greedy qualifiers *?, +?, ?? or {m, n}? match as littile text as possible
    '''
    pass



