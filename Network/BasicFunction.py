'''包含公用的函数'''
import random
def randomcolor():
    colorArr=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color=""
    for i in range(6):
        color+=colorArr[random.randint(0,14)]
    return '#'+color


# 清空所有变量
def clear_all():
    #Clears all the variables from the workspace of the spyder application.
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue
        del globals()[var]
        