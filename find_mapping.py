#!/usr/bin/env python
import subprocess
import common
import sys
import re
import os

file_regex = re.compile('Input:(.*)')
line_regex = re.compile('Line:(.*)')
column_regex = re.compile('Column:(.*)')


def find_mapping(annotations, original):
    mappings = []
    for annotation in annotations:
        try:
            text = subprocess.check_output(['synctex', 'edit', '-o',
                                            str(annotation.page) + ':' + str(annotation.x) + ':' +
                                            str(annotation.y) + ':' + original])
        except subprocess.CalledProcessError:
            sys.exit('No SyncTeX file found?')

        (file, line, column) = parse_synctex_output(text)
        # get relative part of path and then move it relative to the directory the original file is in
        # This only works when the tex file was compiled using TeXstudio which creates file paths like this path-to-folder/./texfile.tex which allows us to detect the root of this project
        # Does not work with the LaTeX Workshop plugin for VS Code
        file = os.path.dirname(original) + file.split('.', 1)[1]

        mappings.append(common.Mapping(file, line, column))
    return mappings


def parse_synctex_output(text):
    text = text.decode('utf-8').splitlines()
    for part in text:
        file_match = file_regex.match(part)
        if file_match:
            file = file_match.group(1)

        line_match = line_regex.match(part)
        if line_match:
            line = line_match.group(1)

        column_match = column_regex.match(part)
        if column_match:
            column = column_match.group(1)

    return (file, line, column)
