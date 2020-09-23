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
            isdir = str(os.path.getsize(path + '\\' + i)) + 'B'
        content += str(index) + '.  ' + isdir  + '\t' + i + '\n'
        index += 1
    return content

#       Обходит дерево каталогов, начиная с корневого
filecount = 0
def bypass(path, size = 0):
    global filecount
    try:
        print(str_content(path))
        None
    except PermissionError: None

    current = 0
    for file in os.listdir(path):
        try:
            if os.path.isdir(path + '\\' + file):
                print('\tDown to: ', file)
                size = bypass(path + '\\' + file, size)
                print('\tUp to: ', path)
            else:
                current = os.path.getsize(path + '\\' + file)
                filecount += 1
                size += current
            print(size)
        except PermissionError: continue
    return size

def sbytes(bytes):
    return bytes / filecount
#           Зона глобальной видимости
bytes = bypass(path)

print('\n')
print(get_kib(sbytes(bytes)))
#print((1746 + 9307472 + 12242 + 652601 + 282))
