# PDFAnnoTeX
This script extracts annotations from a PDF file and tries to add them at the correct place in the original LaTeX source files.

The usecase is that you can send your compiled PDF to friends unfamiliar with LaTeX that want to proofread your thesis. They then add lots of annotations to the PDF and send it back to you. Instead of searching through the PDF for annotations, they are extracted by this script and added into the corresponding LaTeX source code. You can then read the annotations in your LaTeX editor and make the suggested changes right there.

## Requirements
This script is written in Python 3. 
It uses the `popplerqt5`, `pypdf`, `pymupdf`, or `pdfminer` to extract the annotations. The `pdfminer` implementation is based on https://github.com/0xabu/pdfannots.
It needs the `synctex` binary to find the correct source files.

## Usage
The idea is to have the LaTeX source code and the corresponding SyncTeX file (extension `.synctex` or `.synctex.gz`) under version control with git. When you create a PDF to send to a friend, you create a commit and note the commit somewhere. When your friend sends you their annotated PDF file, you go back to that commit and run this script by passing it the annotated file and the location of the originally created pdf file (so the script can find the corresponding synctex file). This will insert the annotations as comments in the LaTeX source code. Then you commit these changes to a new branch and merge that branch with your current `HEAD`. This way you get the annotations in your current version and you can implement the suggested changes.

```
pdfannotex.py paper_annotated.pdf -o path/to/paper.pdf
```

## Limitations
This script is currently limited to placing comments on the line above the one where the annotation was placed. This is due to the current limitations of synctex. This could be expanded in the future to allow for graphical notes in the compiled PDF which could highlight the region of highlight annotations (see [issue #1](https://github.com/bitowl/pdfannotex/issues/1)).


