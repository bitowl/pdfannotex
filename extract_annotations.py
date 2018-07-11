#!/usr/bin/env python
from popplerqt5 import Poppler
import sys
import PyQt5
import common


def extract_annotations(file):
    extracted_annotations = []
    doc = Poppler.Document.load(file)
    total_annotations = 0
    for i in range(doc.numPages()):
        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        for annotation in annotations:
            if is_created_annotation(annotation):
                total_annotations += 1
                extracted = common.Annotation(annotation.author(),
                                                annotation.contents(), i + 1, annotation.boundary().x() * pwidth,
                                                annotation.boundary().y() * pheight)
                extracted_annotations.append(extracted)

            # TODO store additional information for highlight annotations
#               if(isinstance(annotation, Poppler.HighlightAnnotation)):
#                    print('== Annotation ==')
#                    print(annotation.contents() + ': ')
#
#                    quads = annotation.highlightQuads()
#                    txt = ''
#                    for quad in quads:
#                        rect = (quad.points[0].x() * pwidth,
#                                quad.points[0].y() * pheight,
#                                quad.points[2].x() * pwidth,
#                                quad.points[2].y() * pheight)
#                        bdy = PyQt5.QtCore.QRectF()
#                        bdy.setCoords(*rect)
#                        txt = txt + page.text(bdy) + ' '
#                    print('========= ANNOTATION =========')
#                    print(txt)

    if total_annotations > 1:
        print(str(total_annotations) + ' annotations found.')
    elif total_annotations == 1:
        print('1 annotation found.')
    else:
        print('No annotations found.')
    return extracted_annotations


def is_created_annotation(annotation):
    # TODO exclude other types of annotations that would not be created by a reviewer
    return isinstance(annotation, Poppler.Annotation) and annotation.subType() != Poppler.Annotation.SubType.ALink
