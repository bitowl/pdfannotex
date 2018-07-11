#!/usr/bin/env python
from extractannotations import extract_annotations
from createmapping import create_mapping
from insertlatexcomments import insert_latex_comments
import argparse

def parseArguments():
    parser = argparse.ArgumentParser(description = 'Extract annotations from PDF file and insert them in corresponding LaTeX code')
    parser.add_argument('file', help='PDF file containing the annotations')
    parser.add_argument('--orig', '-o', metavar='PATH', help='Location of the original output pdf', dest='original')
    return parser.parse_args()

def main():
    args = parseArguments()
    # fill defaults
    original = args.original
    if original is None:
        original = args.file
    # start process
    annotations = extract_annotations(args.file)
    mapping = create_mapping(annotations, original)
    insert_latex_comments(annotations, mapping)

if __name__ == "__main__":
    main()


