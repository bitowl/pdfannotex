#!/usr/bin/env python


class Annotation:
    author = 'unknown'
    text = ''
    page = -1  # starting at 1
    x = -1
    y = -1
    # TODO for highlight: boxes, highlighted text

    def __init__(self, author, text, page, x, y):
        self.author = author
        self.text = text
        self.page = page
        self.x = x
        self.y = y

    def __repr__(self):
        return self.text + '(' + str(self.page) + ':' + str(self.x) + ',' + str(self.y) + ')'

    def get_latex_comment(self, prefix_format='Annotation from {author}: {text}'):
        text = prefix_format.format(author=self.author, text=self.text)
        return '% ' + '% '.join(text.splitlines(True)) + '\n'


class Mapping:
    file = ''
    line = -1
    column = -1

    def __init__(self, file, line, column):
        self.file = file
        self.line = int(line)
        self.column = int(column)

    def __repr__(self):
        return self.file + ':' + str(self.line) + ':' + str(self.column)
