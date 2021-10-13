import os
from sys import argv

path = argv[len(argv) - 1]

#    Присваивает глобальной переменной path значение пути,
#    в котором _расположен_запускаемый_файл_скрипта_.
#
#    Если же этого действия не делать, то путь будет считаться относительно
#    той директории в которой _запускается_скрипт_.

    # -> path = str(os.path.dirname(__file__)) + "\\" + str(path)


def get_in_mb(size_in_bytes):
    return size_in_bytes / pow(1024, 2)


def get_in_kib(size_in_bytes):
    return size_in_bytes / 1024


#=============================================================================#
#                                 Обход папок                                 #
#=============================================================================#

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
def bypass(path, size = 0):
    global filecount
    global skipped

#    try:
#        print(str_content(path))
#        None
#    except PermissionError: None

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

def sbytes(bytes):
    return bytes / filecount

#           Зона глобальной видимости
bytes = bypass(path)

print()
print('Analyzed data size:', str(bytes) + 'B')
print('Files:', filecount, '\n')
print('Skipped system directories:', skipped)

for i in sysdir:
    print(i)

print()
bytes = sbytes(bytes)
print('Average file size', str(round(get_in_kib(bytes), 2)) + 'KB')


if __name__ == '__main__':
    pass
