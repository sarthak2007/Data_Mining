from helper import *
from collections import deque

def bfs(adj):
    res = []
    category_id = 1
    q = deque()
    visited = set()

    q.append('subject')
    visited.add('subject')

    while q:
        u = q.popleft()
        res.append([u, 'C{:04d}'.format(category_id)])
        category_id += 1

        adj[u].sort()
        for v in adj[u]:
            if v not in visited:
                q.append(v)
                visited.add(v)            

    return res


with open('{}categories.tsv'.format(input_dir1), 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')

    adj = {}
    edges = set()
    for line in tsvreader:
        if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
            continue

        category = line[1].split('.')
        prev = category[0]
        for i in range(1,len(category)):
            curr = prev + '.' + category[i]
            if (prev, curr) in edges:
                prev = curr
                continue
            if prev not in adj:
                adj[prev] = []
            adj[prev].append(curr)

            if curr not in adj:
                adj[curr] = []
            adj[curr].append(prev)
            
            edges.add((prev, curr))
            prev = curr
    
res = bfs(adj)

fields = ['Category_Name', 'Category_ID']
output('category-ids.csv', res, fields, sort = True)