#!/usr/bin/env python
''' A simple proofread program for scientific papers
this script deals with rule based suggestions for remove/replace
by LongGang Pang from UC Berkeley'''
import os
import argparse

parser = argparse.ArgumentParser(description='Proofread scientific papers to make it brief and simple')
parser.add_argument('filenames', metavar='f', type=str, nargs='+',
                    help='one file or a list of files for analysis')
parser.add_argument('--report_long_subjects', action='store_true',
        help='Principle 10: avoid long subjects or many words before the subject. Default=False')
parser.add_argument('--report_interruptions', action='store_true',
        help='Principle 11: avoid interruptions between subject and verb and between verb and object. Default=False')
parser.add_argument('--report_noun_clusters', action='store_true',
        help='Principle 18: avoid noun clusters. Default=False')
parser.add_argument('--report_sentence_fragments', action='store_true',
        help='Avoid sentence fragments where a subject or verb is missing. Default=False')
parser.add_argument('--check_grammars', action='store_true',
        help='Check grammar using online api ginger. Default=False')
parser.add_argument('--check_passive', action='store_true',
        help='Print all passive sentences, try active voice. Default=False')
parser.add_argument('--check_all', action='store_true',
        help='Check all the implemented principles. Default=False')
args = parser.parse_args()


if __name__ == '__main__':
    for fname in args.filenames:
        from rule1to6_words import report_wrong_words
        report_wrong_words(fname, verbose=True)

        if args.check_all:
            args.report_long_subjects = True
            args.report_interruptions = True
            args.report_noun_clusters = True
            args.report_sentence_fragments = True
            args.check_grammars = True
            args.check_passive = True

        if args.report_long_subjects:
            from rule10_long_subject import report_long_subjects
            from rule10_long_subject import principle, example
            print(principle)
            print(example)
            report_if_longer_than = 20
            report_long_subjects(fname, report_if_longer_than)

        if args.report_interruptions:
            from rule11_interruption import report_interruptions
            from rule11_interruption import principle, example
            print(principle)
            print(example)
            report_if_longer_than = 10
            report_interruptions(fname, report_if_longer_than)

        # e.g., the pair correlation and alpha clustering studies
        if args.report_noun_clusters:
            from rule18_noun_cluster import report_noun_clusters
            from rule18_noun_cluster import principle, example
            print(principle)
            print(example)
            report_if_longer_than = 4
            report_noun_clusters(fname, report_if_longer_than)

        # do not recommend if the input file is difficult to sentencizer
        if args.report_sentence_fragments:
            print("Warning: reporting sentence fragments is still experimental feature")
            print("I do not recommend it if the input file is difficult to sentencize")
            from rule_sentence_fragment import report_sentence_fragments
            from rule_sentence_fragment import principle, example
            print(principle)
            print(example)
            report_sentence_fragments(fname)

        if args.check_grammars:
            from check_grammar import check_grammars
            from check_grammar import principle, example
            print(principle)
            print(example)
            check_grammars(fname)

        if args.check_passive:
            from rule_passive import check_passive, principle, example
            print(principle)
            print(example)
            check_passive(fname)
