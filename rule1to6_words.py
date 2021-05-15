import re
import json
from color_print import *

# read rules from json file
with open("rules.json", "r", encoding="utf-8") as json_data:
    rules = json.load(json_data)

# create new rules by replacing 'is' to 'was', 'has been', ...
def augment(sentence):
    """change 'is' in the sentence to was, has been, 
    should be ... to augment some new sentences
    Args:
      sentence: str, candidate sentence to be removed/replaced
    Return:
      augmented_strs: array of new candidates
    """
    pad_sentence = " " + sentence + " "
    augmented_str = [pad_sentence]
    if 'is' in pad_sentence:
        index = pad_sentence.find("is")
        reps = ["was", "have been", "has been", "had been", "should be"]
        for replace_candidate in reps:
            new_str = pad_sentence[:index]
            new_str += replace_candidate
            new_str += pad_sentence[index+2:]
        augmented_str.append(new_str)
    return augmented_str


def get_context(src_text, index):
    '''get the full sentence that contain the position index'''
    stop_puncs = ['.', ',', '!', '?', ';', ':', '\n']
    istart = max([src_text[:index].rfind(st) for st in stop_puncs])
    iend = min([src_text[index:].find(st) for st in stop_puncs if src_text[index:].find(st)!=-1])
    return istart, iend
        
# create suggestions for sentences to remove
def suggest_remove(file_path, to_remove, verbose=True):
    with open(file_path, "r", encoding="utf-8") as fsrc:
        src_text = fsrc.read().lower()
    suggestions = []
    for item in to_remove:
        for s in augment(item):
            if s not in src_text: continue
            suggestions.append(color_red("remove: "+s))
            if verbose:
                indices = [m.start() for m in re.finditer(s, src_text)]
                for index in indices:
                    istart, iend = get_context(src_text, index)
                    ctx = src_text[istart+1:index]+color_red(src_text[index:index+len(s)])
                    ctx += src_text[index+len(s):index+iend]
                    suggestions.append(ctx)
    return suggestions


# create suggestions for sentences to replace
def suggest_replace(file_path, to_replace, verbose=True):
    with open(file_path, "r", encoding="utf-8") as fsrc:
        src_text = fsrc.read().lower()
    suggestions = []
    for key, value in to_replace.items():
        for s in augment(key):
            if s not in src_text: continue
            suggestions.append(color_red("replace: "+s)+" ---> "+color_magenta(value))
            if verbose:
                indices = [m.start() for m in re.finditer(s, src_text)]
                for index in indices:
                    istart, iend = get_context(src_text, index)
                    ctx = src_text[istart+1:index]+color_red(src_text[index:index+len(s)])
                    ctx += src_text[index+len(s):index+iend]
                    suggestions.append(ctx)
    return suggestions


def report_wrong_words(fname, verbose=True):
    '''report problematic words that are not simple, not precise, sexial, or needless'''
    to_remove = rules["to_remove"]
    to_replace = rules["to_replace"]
    sug1 = suggest_remove(fname, to_remove, verbose)
    sug2 = suggest_replace(fname, to_replace, verbose)
    suggestions = sug1 + sug2
    # if no suggestions, continue to process next file
    if len(suggestions) == 0: return
    # otherwise print suggestions to screen
    print(color_blue("******************************************************"))
    print("Words suggestions for ", color_cyan(fname.split('/')[-1]))
    for suggestion in suggestions:
        print(suggestion)
        print("")
