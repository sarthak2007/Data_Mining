from helper import *

with open('{}articles.tsv'.format(input_dir1), 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')

    res = []
    article_id = 1
    for line in tsvreader:
        if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
            continue

        article_name = line[0]
        res.append([article_name, 'A{:04d}'.format(article_id)])
        article_id += 1


fields = ['Article_Name', 'Article_ID']
output('article-ids.csv', res, fields, sort = True)