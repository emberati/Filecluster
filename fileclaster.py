import os
from sys import argv

path = argv[len(argv) - 1]

def main():
    global path

#    Присваивает глобальной переменной path значение пути,
#    в котором _расположен_запускаемый_файл_скрипта_.
#
#    Если же этого действия не делать, то путь будет считаться относительно
#    той директории в которой _запускается_скрипт_.

    # -> path = str(os.path.dirname(__file__)) + "\\" + str(path)

    size_ = os.path.getsize(path)

    mib = get_mib(size_)
    kib = get_kib(size_)

    print("File size is " + str(round(mib, 4)) + "MB.");
    print("File size is " + str(round(kib, 4)) + "KB.");
    print("File size is " + str(size_) + "B.");


def get_mib(size_in_bytes):
    return size_in_bytes / pow(1024, 2)

def get_kib(size_in_bytes):
    return size_in_bytes / 1024


#=============================================================================#
#                                 Обход папок                                 #
#=============================================================================#

#       Возвращает отформатированный список файлов и папок директории
def str_content(path):
    content = os.path.abspath(path) + '\n'
    isdir = ''
    index = 0

    for i in os.listdir(path):
        if os.path.isdir(path + '\\' + i):
            isdir = '<DIR>'
        else:
            isdir = '\t'
        content += str(index) + '.  ' + isdir  + '\t' + i + '\n'
        index += 1
    return content

#       Обходит дерево каталогов, начиная с корневого
def bypass(path, level = 0):
    print(str_content(path))
    #print('Level', str(level) + ':', 'Content:', os.listdir(path))
    for file in os.listdir(path):
        if os.path.isdir(path + '\\' + file):
            print('Down to: ', file)
            bypass(path + '\\' + file, level + 1)
            print('Up to: ', path)
        



#           Зона глобальной видимости
bypass(path)
