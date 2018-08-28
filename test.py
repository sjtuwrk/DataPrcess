import os

mobile = 'efg'
file = r'a.txt'
with open(file, 'a+') as f:
     f.write(mobile+'\n')   #加\n换行显示

