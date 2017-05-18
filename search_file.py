import os

def search(s, path='.'):
    '''
    http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431925324119bac1bc7979664b4fa9843c0e5fcdcf1e000
    编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
    '''
    result = []
    for file in os.listdir(path):
        fullname = os.path.join(path,file)
        if os.path.isfile(fullname):
            if s in file:
                result.append(fullname)
        else:
            result += search(s,fullname)
    return result
