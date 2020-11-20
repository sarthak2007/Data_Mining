from helper import *
from collections import deque

def bfs(src, pred, adj):
    q = deque()
    visited = set()
    pred[src] = {}

    q.append(src)
    visited.add(src)
    pred[src][src] = "root"

    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in visited:
                q.append(v)
                visited.add(v)            
                pred[src][v] = u

def compute_shortest_paths(adj):
    pred = {}
    for u in adj:
        bfs(u, pred, adj)
    return pred

def get_category_ids():
    with open('{}category-ids.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        catids = {}
        for line in csvreader:
            catids[line['Category_ID']] = [0]*4
    return catids

def update_res(path, artid_to_catid, res, res_subtree, catname_to_id, catid_to_name, index):
    dup = set()
    dup_subtree = set()
    for art_id in path:
        for cat_id in artid_to_catid[art_id]:
            if cat_id not in dup:
                dup.add(cat_id)
                res[cat_id][index] += 1
            res[cat_id][index+1] += 1            

            cat_name = catid_to_name[cat_id]
            while True:
                cat_id = catname_to_id[cat_name]
                if cat_id not in dup_subtree:
                    dup_subtree.add(cat_id)
                    res_subtree[cat_id][index] += 1
                res_subtree[cat_id][index+1] += 1  

                if len(cat_name.split('.')) == 1:
                    break
                cat_name = cat_name.rsplit('.', 1)[0]


def get_path(src, dest, pred):
    path = []
    curr = dest
    path.append(curr)
    while pred[src][curr] != "root":
        path.append(pred[src][curr])
        curr = pred[src][curr]
    path.reverse()

    return path

def compute_paths_and_times(artname_to_id, artid_to_catid, shortest_path, pred, catname_to_id, catid_to_name):
    res = get_category_ids()
    res_subtree = get_category_ids()
    with open('{}paths_finished.tsv'.format(input_dir1), 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        
        for line in tsvreader:
            if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
                continue

            path = line[3].split(';')
            src, dest = artname_to_id[path[0]], artname_to_id[path[-1]]
            src_num, dest_num = int(src[1:])-1, int(dest[1:])-1
            
            if shortest_path[src_num][dest_num] == '_':
                continue

            human_path = []
            for x in path:
                if x != "<":
                    human_path.append(x)
                else:
                    human_path.pop()
            human_path = [artname_to_id[x] for x in human_path]
            update_res(human_path, artid_to_catid, res, res_subtree, catname_to_id, catid_to_name, index = 0)

            small_path = get_path(src, dest, pred)
            update_res(small_path, artid_to_catid, res, res_subtree, catname_to_id, catid_to_name, index = 2)
            
    return res, res_subtree

def convert_dict_to_list(res):
    temp = []
    for x, y in res.items():
        temp.append([x] + y)
    return temp


artname_to_id = get_article_ids()
artid_to_catids = get_art_to_cat_ids()
catname_to_id, catid_to_name = get_category_ids_names()
shortest_path = get_shortest_paths()
adj = get_graph(directed = True)
pred = compute_shortest_paths(adj)
res, res_subtree = compute_paths_and_times(artname_to_id, artid_to_catids, shortest_path, pred, catname_to_id, catid_to_name)
res = convert_dict_to_list(res)
res_subtree = convert_dict_to_list(res_subtree)

fields = ['Category_ID','Number_of_human_paths_traversed','Number_of_human_times_traversed','Number_of_shortest_paths_traversed','Number_of_shortest_times_traversed']
output("category-paths.csv", res, fields, sort = True)
output("category-subtree-paths.csv", res_subtree, fields, sort = True)