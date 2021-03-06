#!/usr/bin/env python
#from extract_poppler import extract_annotations
#from extract_pypdf import extract_annotations
#from extract_mupypdf import extract_annotations
from extract_pdfminer import extract_annotations
from find_mapping import find_mapping
from insert_latex_comments import insert_latex_comments
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Extract annotations from PDF file and insert them in corresponding LaTeX code')
    parser.add_argument('file', help='PDF file containing the annotations')
    parser.add_argument('--orig', '-o', metavar='PATH',
                        help='Location of the original output pdf', dest='original')
    parser.add_argument(
        '--prefix', help='Prefix for the inserted LaTeX comment', default='Annotation from {author}: {text}')
    return parser.parse_args()


def main():
    args = parse_arguments()
    # fill defaults
    original = args.original
    if original is None:
        original = args.file

    # start process
    annotations = extract_annotations(args.file)
    mapping = find_mapping(annotations, original)
    insert_latex_comments(annotations, mapping, args.prefix)


if __name__ == '__main__':
    main()
