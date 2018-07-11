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
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, Poppler.Annotation):
                   # TODO exclude other types of annotations that would not be created by a reviewer
                    if annotation.subType() != Poppler.Annotation.SubType.ALink:
                        total_annotations += 1
                        extracted = common.Annotation(annotation.author(), annotation.contents(), i+1, annotation.boundary().x()*pwidth, annotation.boundary().y()*pheight)
                        extracted_annotations.append(extracted)

                    # TODO store additional information for highlight annotations
 #                   if(isinstance(annotation, Poppler.HighlightAnnotation)):

#                        print('== Annotation ==')
#                        print(annotation.contents() + ': ')
#                        synctex(i+1, 
#
#                        quads = annotation.highlightQuads()
#                        txt = ""
#                        for quad in quads:
#                            rect = (quad.points[0].x() * pwidth,
#                                    quad.points[0].y() * pheight,
#                                    quad.points[2].x() * pwidth,
#                                    quad.points[2].y() * pheight)
#                            bdy = PyQt5.QtCore.QRectF()
#                            bdy.setCoords(*rect)
#                            txt = txt + page.text(bdy) + ' '

                        #print("========= ANNOTATION =========")
#                        print(txt)

    if total_annotations > 0:
        print (str(total_annotations) + " annotation(s) found")
    else:
        print ("no annotations found")
    return extracted_annotations

def main():
    print()

if __name__ == "__main__":
    main()
