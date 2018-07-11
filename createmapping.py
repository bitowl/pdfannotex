#!/usr/bin/env python
import subprocess
import common
import sys
import re

file_regex = re.compile('Input:(.*)')
line_regex = re.compile('Line:(.*)')
column_regex = re.compile('Column:(.*)')

def create_mapping(annotations, original):
 
    mappings=[]
    for annotation in annotations:
        try:
            text = subprocess.check_output(['synctex', 'edit', '-o', str(annotation.page) + ':' + str(annotation.x) + ':' + str(annotation.y) + ':' + original])
        except subprocess.CalledProcessError:
            sys.exit('No SyncTeX file found?')
        (file, line, column) = decodeText(text)
        mappings.append(common.Mapping(file, line, column))
    return mappings

def decodeText(text):
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

def main():
    print()

if __name__ == "__main__":
    main()

