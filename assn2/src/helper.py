import csv

input_dir1 = '../data/wikispeedia_paths-and-graph/'
input_dir2 = '../data/output/'
output_dir = '../data/output/'

def output(filename, res, fields, sort):
    with open('{}{}'.format(output_dir, filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter = csv.writer(csvfile, lineterminator='\n')
        csvwriter.writerow(fields)
        if sort:
            res.sort()
        csvwriter.writerows(res)

def get_graph(directed):
    with open('{}article-ids.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        adj = {}
        for line in csvreader:
            adj[line['Article_ID']] = []

    with open('{}edges.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for line in csvreader:
            u = line['From_ArticleID']
            v = line['To_ArticleID']
            if v not in adj[u]:
                adj[u].append(v)

            if not directed:
                if u not in adj[v]:
                    adj[v].append(u)

    return adj

def get_article_ids():
    with open('{}article-ids.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        name_to_id = {}
        for line in csvreader:
            name_to_id[line['Article_Name']] = line['Article_ID']
    return name_to_id

def get_category_ids_names():
    with open('{}category-ids.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        name_to_id, id_to_name = {}, {}
        for line in csvreader:
            name_to_id[line['Category_Name']] = line['Category_ID']
            id_to_name[line['Category_ID']] = line['Category_Name']
    return name_to_id, id_to_name

def get_shortest_paths():
    with open('{}shortest-path-distance-matrix.txt'.format(input_dir1), 'r') as textfile:

        shortest_path = []
        lines = textfile.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            shortest_path.append(line)
    return shortest_path

def get_art_to_cat_ids():
    with open('{}article-categories.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        artid_to_catid = {}
        next(csvreader)
        for line in csvreader:
            artid_to_catid[line[0]] = line[1:]
    return artid_to_catid