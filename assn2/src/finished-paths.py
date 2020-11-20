from helper import *

def compute_path_lengths(artname_to_id, shortest_path):
    with open('{}paths_finished.tsv'.format(input_dir1), 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')

        res_back, res_no_back = [], []
        for line in tsvreader:
            if len(line) == 0 or (len(line[0]) > 0 and line[0][0] == '#'):
                continue

            path = line[3].split(';')
            src, dest = artname_to_id[path[0]], artname_to_id[path[-1]]
            src_num, dest_num = int(src[1:])-1, int(dest[1:])-1
            
            if shortest_path[src_num][dest_num] == '_' or shortest_path[src_num][dest_num] == '0':
                continue
            human_path_length = len(path)-1
            shortest_path_length = int(shortest_path[src_num][dest_num])
            ratio = human_path_length/shortest_path_length
            res_back.append([human_path_length, shortest_path_length, ratio])

            back_clicks = path.count("<")
            human_path_length = len(path)-1 - 2*back_clicks
            ratio = human_path_length/shortest_path_length
            res_no_back.append([human_path_length, shortest_path_length, ratio])
    return res_back, res_no_back


artname_to_id = get_article_ids()
shortest_path = get_shortest_paths()
res_back, res_no_back = compute_path_lengths(artname_to_id, shortest_path)

fields = ['Human_Path_Length', 'Shortest_Path_Length', 'Ratio']
output("finished-paths-back.csv", res_back, fields, sort = False)
output("finished-paths-no-back.csv", res_no_back, fields, sort = False)