from helper import *
import sys
from collections import deque

sys.setrecursionlimit(10**5)

def dfs(u, adj, visited, id_conn_comp, num):
    id_conn_comp[u] = num
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v, adj, visited, id_conn_comp, num)

def calc_edges(vertices, adj):
    edges = 0
    for u in vertices:
        edges += len(adj[u])
    return edges // 2

def bfs(u, adj):
    res = 0
    q = deque()
    visited = set()

    q.append((u, 0))
    visited.add(u)

    while q:
        u, d = q.popleft()
        res = max(res, d)
        for v in adj[u]:
            if v not in visited:
                q.append((v, d+1))
                visited.add(v)            

    return res

def calc_diameter(vertices, adj):
    diameter = 0
    for u in vertices:
        diameter = max(diameter, bfs(u, adj))
    return diameter


adj = get_graph(directed = False)
# compute connected components
res = []
visited = set()
id_conn_comp = {}
num = 0
for u in adj:
    if u not in visited:
        dfs(u, adj, visited, id_conn_comp, num)
        num += 1

conn_comp = {}
for u in adj:
    if id_conn_comp[u] not in conn_comp:
        conn_comp[id_conn_comp[u]] = []
    conn_comp[id_conn_comp[u]].append(u)

for _, vertices in conn_comp.items():
    nodes = len(vertices)
    edges = calc_edges(vertices, adj)
    diameter = calc_diameter(vertices, adj)
    res.append([nodes, edges, diameter])

fields = ['Nodes', 'Edges', 'Diameter']
output('graph-components.csv', res, fields, sort = True)