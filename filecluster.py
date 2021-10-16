import os
from config import config
from json import JSONEncoder, JSONDecoder
from enum import Enum

ntfs = [4096 * i for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]


class Units(Enum):
    BYTES     = 1
    KILOBYTES = 1024
    MEGABYTES = 1048576
    GIGABYTES = 1073741824


def convert(size, a, b):
    if a.value > b.value:
        cf = a.value / b.value
        return size * cf
    else:
        cf = b.value / a.value
        return size / cf


def recommend(average_size):
    recommended_cluster_i = 0
    _len = len(ntfs)
    _min = ntfs[_len-1]
    for i in range(_len):
        if abs(ntfs[i] - average_size) < _min:
            _min = abs(ntfs[i] - average_size)
            recommended_cluster_i = i
    return ntfs[recommended_cluster_i - 1]


class Session:
    """
    Session object stores result values after scanning specified directory, such as summary size of all scanned files,
    count of scanned files, or skipped files (because of PermissionError).

    In other words, it's stores result of scanning one directory. One Session obj - one directory.
    """
    overall_count = 0
    overall_size = 0
    ignored_count = 0
    ignored_files = []

    def __init__(self, __path__: str):
        self.path = __path__

    def bypass(self, path, overall_size=0, overall_count=0, ignored_files=0, ignored_count=0):
        #    try:
        #        print(str_content(path))
        #        None
        #    except PermissionError: None

        for file in os.listdir(path):
            node = path + '\\' + file
            try:
                if os.path.isdir(node):
                    print('\tDown to: ', file)
                    self.bypass(node, overall_size)
                    print('\tUp to: ', path)
                else:
                    node_size = os.path.getsize(node)
                    self.overall_count += 1
                    self.overall_size += node_size
            except PermissionError:
                self.ignored_files.append(node)
                self.ignored_count += 1
                continue

    def __repr__(self):
        conv_overall = convert(self.overall_size, Units.BYTES, Units.KILOBYTES)

        return f'Analyzed data size: {round(conv_overall, 2)}KB ({self.overall_size}B) \n' \
               f'Files: {self.overall_count} \n' \
               f'Skipped directories: {self.ignored_count}'


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

# def str_content(path):
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
    size_av = fc.session.overall_size / fc.session.overall_count
    size_av = round(convert(size_av, Units.BYTES, Units.KILOBYTES))
    print('Average file size', f'{size_av}KB')


if __name__ == '__main__':
    pass
    main_new()
