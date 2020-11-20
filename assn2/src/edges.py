from helper import *

with open('{}shortest-path-distance-matrix.txt'.format(input_dir1), 'r') as textfile:

    res = []
    u = 1
    lines = textfile.readlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        for v in range(len(line)):
            if line[v] == '1':  
                res.append(['A{:04d}'.format(u), 'A{:04d}'.format(v+1)])
        
        u += 1

fields = ['From_ArticleID', 'To_ArticleID']
output('edges.csv', res, fields, sort = False)