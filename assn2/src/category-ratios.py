from helper import *

def get_ratios():
    ratios = []
    with open('{}finished-paths-no-back.csv'.format(input_dir2), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for line in csvreader:
            ratios.append(int(line['Human_Path_Length'])/int(line['Shortest_Path_Length']))
    return ratios

def compute(art_id, artid_to_catid, catname_to_id, catid_to_name):
    categories = set()
    for cat_id in artid_to_catid[art_id]:

        cat_name = catid_to_name[cat_id]
        while True:
            cat_id = catname_to_id[cat_name]
            if cat_id not in categories:
                categories.add(cat_id)

            if len(cat_name.split('.')) == 1:
                break
            cat_name = cat_name.rsplit('.', 1)[0]

    return categories

def compute_ratios(artname_to_id, artid_to_catid, catname_to_id, catid_to_name, res, ratios):

    with open('{}paths_finished.tsv'.format(input_dir1), 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')

        line_num = 0
        for line in tsvreader:
            if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
                continue

            if len(line[3].split(';')) == 1:
                continue

            if line[3] == "Bird;Wikipedia_Text_of_the_GNU_Free_Documentation_License":
                continue
            
            src = line[3].split(';')[0]
            dest = line[3].split(';')[-1]

            src_cats = compute(artname_to_id[src], artid_to_catid, catname_to_id, catid_to_name)
            dest_cats = compute(artname_to_id[dest], artid_to_catid, catname_to_id, catid_to_name)
            
            for src_cat in src_cats:
                for dest_cat in dest_cats:
                    if (src_cat, dest_cat) not in res:
                        res[(src_cat, dest_cat)] = [0, 0]
                    res[(src_cat, dest_cat)][0] += ratios[line_num]
                    res[(src_cat, dest_cat)][1] += 1

            line_num += 1

def convert_dict_to_list(res):
    temp = []
    for x, y in res.items():
        src, dest = x
        sum_ratio, cnt = y[0], y[1]
        avg_ratio = sum_ratio/cnt
        temp.append([src,dest,avg_ratio])
    return temp


artname_to_id = get_article_ids()
artid_to_catids = get_art_to_cat_ids()
catname_to_id, catid_to_name = get_category_ids_names()

ratios = get_ratios()
res = {}
compute_ratios(artname_to_id, artid_to_catids, catname_to_id, catid_to_name, res, ratios)
res = convert_dict_to_list(res)
fields = ['From_Category','To_Category','Ratio_of_human_to_shortest']
output("category-ratios.csv", res, fields, sort = True)