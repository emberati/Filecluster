import os
from cmdparse import path
from json import JSONEncoder, JSONDecoder


def get_in_mb(size_in_bytes):
    return size_in_bytes / pow(1024, 2)


def get_in_kib(size_in_bytes):
    return size_in_bytes / 1024


class Session:
    count_of_files          = None
    overall_size            = None
    count_of_skipped_files  = None
    skipped_files           = None

    def __init__(self, __path__):
        self.path = __path__


class SessionEncoder(JSONEncoder):
    pass


class SessionDecoder(JSONDecoder):
    pass


# ============================================================================= #
#                                 Обход папок                                   #
# ============================================================================= #

#       Возвращает отформатированный список файлов и папок директории

#def str_content(path):
#    content = os.path.abspath(path) + '\n'
#    isdir = ''
#    index = 0
#    for i in os.listdir(path):
#        if os.path.isdir(path + '\\' + i):
#            isdir = '<DIR>'
#        else:
#            isdir = str(os.path.getsize(path + '\\' + i)) + 'B'
#        content += str(index) + '.  ' + isdir  + '\t' + i + '\n'
#        index += 1
#    return content

#       Обходит дерево каталогов, начиная с корневого
filecount = 0
skipped = 0
sysdir = []


def bypass(path, size=0):
#    try:
#        print(str_content(path))
#        None
#    except PermissionError: None
    global filecount
    global skipped
    global sysdir

    current = 0
    for file in os.listdir(path):
        node = path + '\\' + file
        try:
            if os.path.isdir(node):
                print('\tDown to: ', file)
                size = bypass(node, size)
                print('\tUp to: ', path)
            else:
                current = os.path.getsize(node)
                filecount += 1
                size += current
        except PermissionError:
            sysdir.append(node)
            skipped += 1
            continue
    return size


def average_file_size(bytes):
    return bytes / filecount


#           Зона глобальной видимости
def main_old():
    bytes = bypass(path)

    print()
    print('Analyzed data size:', str(bytes) + 'B')
    print('Files:', filecount, '\n')
    print('Skipped system directories:', skipped)

    for i in sysdir:
        print(i)

    print()
    bytes = average_file_size(bytes)
    print('Average file size', str(round(get_in_kib(bytes), 2)) + 'KB')


def main_new():
    s = Session(path)
    size = bypass(s.path)

    print('Analyzed data size:', str(size) + 'B')
    print('Files:', filecount, '\n')
    print('Skipped system directories:', skipped)

    for i in sysdir:
        print(i)

    print()
    av = average_file_size(size)
    print('Average file size', str(round(get_in_kib(av), 2)) + 'KB')


if __name__ == '__main__':
    # main_old()
    main_new()
