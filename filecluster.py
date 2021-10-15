import os
from config import config
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
    count_of_files          = 0
    overall_size            = 0
    count_of_skipped_files  = 0
    skipped_files           = []

    def __init__(self, __path__: str):
        self.path = __path__

    def bypass(self, path, size=0):
        #    try:
        #        print(str_content(path))
        #        None
        #    except PermissionError: None

        for file in os.listdir(path):
            node = path + '\\' + file
            try:
                if os.path.isdir(node):
                    print('\tDown to: ', file)
                    self.bypass(node, size)
                    print('\tUp to: ', path)
                else:
                    node_size = os.path.getsize(node)
                    self.count_of_files += 1
                    self.overall_size += node_size
            except PermissionError:
                self.skipped_files.append(node)
                self.count_of_skipped_files += 1
                continue

    def __repr__(self):
        return f'Analyzed data size: {self.overall_size}B \n' \
               f'Files: {self.count_of_files} \n' \
               f'Skipped directories: {self.count_of_skipped_files}'


class SessionEncoder(JSONEncoder):
    pass


class SessionDecoder(JSONDecoder):
    pass


class FileCluster:
    def __init__(self):
        self.session = Session(config.path)

    def scan(self):
        self.session.bypass(self.session.path)

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

# Зона глобальной видимости
def main_new():
    fc = FileCluster()
    fc.scan()
    print(fc.session)
    print()
    print('Average file size', str(round(fc.session.overall_size / fc.session.count_of_files, 2)) + 'KB')


if __name__ == '__main__':
    main_new()
