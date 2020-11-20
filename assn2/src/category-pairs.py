from helper import *

def get_catids(art_name, catname_to_id, artid_to_catid, artname_to_id):
    if art_name not in artname_to_id:
        return [catname_to_id['subject']]
    else:
        return artid_to_catid[artname_to_id[art_name]]

def compute(art_name, artid_to_catid, catname_to_id, catid_to_name, artname_to_id):
    categories = set()
    for cat_id in get_catids(art_name, catname_to_id, artid_to_catid, artname_to_id):

        cat_name = catid_to_name[cat_id]
        while True:
            cat_id = catname_to_id[cat_name]
            if cat_id not in categories:
                categories.add(cat_id)

            if len(cat_name.split('.')) == 1:
                break
            cat_name = cat_name.rsplit('.', 1)[0]

    return categories

def compute_pairs(artname_to_id, artid_to_catid, catname_to_id, catid_to_name, res, mappings, finished):

    filename = 'paths_unfinished.tsv'
    if finished:
        filename = 'paths_finished.tsv'
    with open('{}{}'.format(input_dir1, filename), 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')

        for line in tsvreader:
            if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
                continue

            if finished:
                if len(line[3].split(';')) == 1:
                    continue

                if line[3] == "Bird;Wikipedia_Text_of_the_GNU_Free_Documentation_License":
                    continue
                
            src = line[3].split(';')[0]
            dest = line[4]
            if finished:
                dest = line[3].split(';')[-1]

            if src not in artname_to_id and src in mappings:
                src = mappings[src]
            if dest not in artname_to_id and dest in mappings:
                dest = mappings[dest]

            index = 0
            if finished:
                index = 1
            src_cats = compute(src, artid_to_catid, catname_to_id, catid_to_name, artname_to_id)
            dest_cats = compute(dest, artid_to_catid, catname_to_id, catid_to_name, artname_to_id)
            
            for src_cat in src_cats:
                for dest_cat in dest_cats:
                    if (src_cat, dest_cat) not in res:
                        res[(src_cat, dest_cat)] = [0, 0]
                    res[(src_cat, dest_cat)][index] += 1

def convert_dict_to_list(res):
    temp = []
    for x, y in res.items():
        src, dest = x
        unfin, fin = y[0], y[1]
        percent_fin, percent_unfin = fin*100/(fin+unfin), unfin*100/(fin+unfin)
        temp.append([src,dest,percent_fin,percent_unfin])
    return temp


artname_to_id = get_article_ids()
artid_to_catids = get_art_to_cat_ids()
catname_to_id, catid_to_name = get_category_ids_names()

mappings = {
    'Adolph_Hitler': 'Adolf_Hitler',
    'Bogota': 'Bogot%C3%A1',
    'C++': 'C%2B%2B',
    'Charlottes_web': 'Charlotte%27s_Web',
    'Kashmir': 'Kashmir_region',
    'Long_peper': 'Long_pepper',
    'Podcast': 'Podcasting',
    'Rss': 'RSS_%28file_format%29'
}

res = {}
compute_pairs(artname_to_id, artid_to_catids, catname_to_id, catid_to_name, res, mappings, finished = False)
compute_pairs(artname_to_id, artid_to_catids, catname_to_id, catid_to_name, res, mappings, finished = True)
res = convert_dict_to_list(res)
fields = ['From_Category','To_Category','Percentage_of_finished_paths','Percentage_of_unfinished_paths']
output("category-pairs.csv", res, fields, sort = True)