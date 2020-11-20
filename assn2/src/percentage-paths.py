from helper import *

def find_percent(filename):
    with open('{}{}'.format(input_dir2, filename), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        res = [0]*12
        total = 0
        for line in csvreader:
            diff = int(line['Human_Path_Length']) - int(line['Shortest_Path_Length'])
            index = min(diff, 11)
            res[index] += 1
            total += 1
        res = [x*100/total for x in res]
    return [res]

res_back = find_percent("finished-paths-back.csv")
res_no_back = find_percent("finished-paths-no-back.csv")

fields = ['Equal_Length','Larger_by_1','Larger_by_2','Larger_by_3','Larger_by_4','Larger_by_5','Larger_by_6','Larger_by_7','Larger_by_8','Larger_by_9','Larger_by_10','Larger_by_more_than_10']
output("percentage-paths-back.csv", res_back, fields, sort = False)
output("percentage-paths-no-back.csv", res_no_back, fields, sort = False)