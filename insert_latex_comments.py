#!/usr/bin/env python
import os


def insert_latex_comments(annotations, mappings):
    tuple_list = list(zip(annotations, mappings))
    # sort by file, then by line
    tuple_list = sorted(tuple_list, key=lambda t: (t[1].file, int(t[1].line)))

    created_files = []
    open_file_name = ''
    file_read = None
    file_write = None
    current_line = 0
    last_line = ''

    for (annotation, mapping) in tuple_list:
        if mapping.file != open_file_name:
            if file_read:
                finish_writing_file(file_read, file_write, last_line)
            # open file
            file_read = open(mapping.file, 'r', encoding='utf-8')
            file_write = open(mapping.file + '.anno', 'w', encoding='utf-8')
            open_file_name = mapping.file
            current_line = 1
            last_line = file_read.readline()
            created_files.append(mapping.file)

        if current_line == mapping.line:
            file_write.write(annotation.get_latex_comment())
            continue
        file_write.write(last_line)

        for line in file_read:
            current_line += 1
            if current_line == mapping.line:
                last_line = line
                file_write.write(annotation.get_latex_comment())
                break
            file_write.write(line)

    finish_writing_file(file_read, file_write, last_line)
    move_files_overriding_originals(created_files)


def finish_writing_file(file_read, file_write, last_line):
    if file_read:
        # Finish the old file
        file_write.write(last_line)
        for line in file_read:
            file_write.write(line)
        file_read.close()
        file_write.close()


def move_files_overriding_originals(created_files):
    for file in created_files:
        os.rename(file + '.anno', file)
        print('Wrote annotations to ' + os.path.normpath(file) + '.')
