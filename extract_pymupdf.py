#!/usr/bin/env python
import sys
import fitz
import common

# Status: Not yet working


# https://github.com/pymupdf/PyMuPDF/issues/318#issuecomment-658781494
_threshold_intersection = 0.9  # if the intersection is large enough.


def _check_contain(r_word, points):
    """If `r_word` is contained in the rectangular area.

    The area of the intersection should be large enough compared to the
    area of the given word.

    Args:
        r_word (fitz.Rect): rectangular area of a single word.
        points (list): list of points in the rectangular area of the
            given part of a highlight.

    Returns:
        bool: whether `r_word` is contained in the rectangular area.
    """
    # `r` is mutable, so everytime a new `r` should be initiated.
    r = fitz.Quad(points).rect
    r.intersect(r_word)

    if r.getArea() >= r_word.getArea() * _threshold_intersection:
        contain = True
    else:
        contain = False
    return contain


def _extract_annot(annot, words_on_page):
    """Extract words in a given highlight.

    Args:
        annot (fitz.Annot): [description]
        words_on_page (list): [description]

    Returns:
        str: words in the entire highlight.
    """
    quad_points = annot.vertices
    quad_count = int(len(quad_points) / 4)
    sentences = ['' for i in range(quad_count)]
    for i in range(quad_count):
        points = quad_points[i * 4: i * 4 + 4]
        words = [
            w for w in words_on_page if
            _check_contain(fitz.Rect(w[:4]), points)
        ]
        sentences[i] = ' '.join(w[4] for w in words)
    sentence = ' '.join(sentences)

    return sentence


def extract_annotations(file):
    extracted_annotations = []
    doc = fitz.open(file)
    for page in doc:
        words = page.getText('words')

        for annot in page.annots():
            print(annot.type, annot.info)
            if annot.type[0] in (8, 9, 10, 11):
                print(_extract_annot(annot, words))
            else:
                print('...')
    return extracted_annotations


# test extracting annotations
if __name__ == '__main__':
    print(extract_annotations(sys.argv[1]))
