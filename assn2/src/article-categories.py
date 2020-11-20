from helper import *

with open('{}category-ids.csv'.format(input_dir2), 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    categoryname_to_id = {}
    for line in csvreader:
        categoryname_to_id[line['Category_Name']] = line['Category_ID']

with open('{}categories.tsv'.format(input_dir1), 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')

    articlename_to_categoryname = {}
    for line in tsvreader:
        if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
            continue
        
        article_name = line[0]
        if article_name not in articlename_to_categoryname:
            articlename_to_categoryname[article_name] = []
        articlename_to_categoryname[article_name].append(line[1])

with open('{}article-ids.csv'.format(input_dir2), 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    res = []
    for line in csvreader:
        categories = [categoryname_to_id['subject']]
        if line['Article_Name'] in articlename_to_categoryname:    
            categories = [categoryname_to_id[x] for x in articlename_to_categoryname[line['Article_Name']]]
            categories.sort()
        
        res.append([line['Article_ID']] + categories)


fields = ['Article_ID', 'Category_ID']
output('article-categories.csv', res, fields, sort = True)