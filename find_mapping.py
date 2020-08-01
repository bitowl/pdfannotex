#!/usr/bin/env python
import subprocess
import common
import sys
import re
import os
import gzip
import ntpath

file_regex = re.compile('Input:(.*)')
line_regex = re.compile('Line:(.*)')
column_regex = re.compile('Column:(.*)')


def find_mapping(annotations, original):

    root_folder = detect_root_folder(original)

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
        file = ntpath.join(ntpath.dirname(original),
                           ntpath.relpath(file, root_folder))

        # Use posix path going forward
        file = file.replace(ntpath.sep, ntpath.altsep)

        mappings.append(common.Mapping(file, line, column))
    return mappings


def detect_root_folder(original):
    # Tries to detect the root folder of the LaTeX project by reading the second line of the synctex file
    with gzip.open(original.replace('.pdf', '.synctex.gz'), 'rt') as f:
        first = f.readline()
        second = f.readline()
        if second.startswith('Input:1:'):
            # We need to use ntpath here, because we are compiling pdfs on Windows and then use PdfAnnoTeX on a Linux server
            return ntpath.dirname(second[8:])

    # No root folder found
    return ''


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
