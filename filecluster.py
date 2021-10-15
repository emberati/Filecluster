import os
import config
from json import JSONEncoder, JSONDecoder


def get_in_mb(size_in_bytes):
    return size_in_bytes / pow(1024, 2)


def get_in_kib(size_in_bytes):
    return size_in_bytes / 1024


class Session:
    """
    Session object stores result values after scanning specified directory, such as summary size of all scanned files,
    count of scanned files, or skipped files (because of PermissionError).

    In other words, it's stores result of scanning one directory. One Session obj - one directory.
    """
    count_of_files          = None
    overall_size            = None
    count_of_skipped_files  = None
    skipped_files           = None

    def __init__(self, __path__: str):
        self.path = __path__

    def get_statistics(self):
        pass


class SessionEncoder(JSONEncoder):
    pass


class SessionDecoder(JSONDecoder):
    pass


class FileCluster:
    sessions = []

    def __init__(self):
        path = config.get_path()
        self.create_session(path)

    def scan(self, fast=True):
        for session in self.sessions:
            session.overall_size = bypass(session.path)


    def create_session(self, path: str):
        self.sessions.append(Session(path))

    def save_session(self, session_id: int):
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

    for file in os.listdir(path):
        node = path + '\\' + file
        try:
            if os.path.isdir(node):
                print('\tDown to: ', file)
                size = bypass(node, size)
                print('\tUp to: ', path)
            else:
                node_size = os.path.getsize(node)
                filecount += 1
                size += node_size
        except PermissionError:
            sysdir.append(node)
            skipped += 1
            continue
    return size


def average_file_size(bytes):
    return bytes / filecount


# Зона глобальной видимости
def main_new():
    path = config.get_path()
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
    main_new()
