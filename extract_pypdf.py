#!/usr/bin/env python
import sys
import PyPDF2
import traceback
import common


def extract_annotations(file):
    extracted_annotations = []

    input1 = PyPDF2.PdfFileReader(open(file, "rb"))
    nPages = input1.getNumPages()

    for i in range(nPages):
        page0 = input1.getPage(i)
        pageHeight = page0['/MediaBox'][3]
        try:
            for iAnnot in page0['/Annots']:
                annot = iAnnot.getObject()
                if annot['/Subtype'] == '/Link':
                    # Ignore links that are created by LaTeX
                    continue
                elif annot['/Subtype'] == '/Popup':
                    # Popups are usually handled at the corresponding highlight
                    continue
                elif annot['/Subtype'] == '/Text' or annot['/Subtype'] == '/Highlight' or annot['/Subtype'] == '/StrikeOut' or annot['/Subtype'] == '/Underline' or annot['/Subtype'] == '/Squiggly':
                    x = annot['/Rect'][0]
                    y = pageHeight - annot['/Rect'][3]
                    if '/Contents' in annot:
                        text = annot['/Contents']
                    else:
                        text = ''
                    extracted = common.Annotation(
                        annot['/T'], text, i + 1, x, y)
                    extracted_annotations.append(extracted)
                else:
                    print('Unknown subtype ' + annot['/Subtype'])

                # print(annot)
                # print('')
        except Exception as e:
            print(e)
            # there are no annotations on this page
            pass

    return extracted_annotations


# test extracting annotations
if __name__ == '__main__':
    print(extract_annotations(sys.argv[1]))
