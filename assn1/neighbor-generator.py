import json
import math

district_ids = json.loads(open("neighbor-districts-modified.json", 'r').read())
neighbors = {}
for x, y in district_ids.items():
    id = x.split('|')[0]
    neighbors[id] = []
    for district in y:
        id2 = district.split('|')[0]
        neighbors[id].append(id2)

def load_data(filename):
    with open(filename, 'r') as f:
        orig_data = {}
        elem = f.readlines()
        for temp in elem:
            district_id = temp.split(',')[0]
            time_id = temp.split(',')[1]
            cases = int(temp.split(',')[2][:-1])
            if district_id not in orig_data:
                orig_data[district_id] = {}
            orig_data[district_id][time_id] = cases
    
    data = {}
    for district_id, x in orig_data.items():
        data[district_id] = {}
        N = len(neighbors[district_id])
        for time_id in x.keys():
            mean = 0
            for neighbor in neighbors[district_id]:
                mean += orig_data[neighbor][time_id]
            mean /= N

            stddev = 0
            for neighbor in neighbors[district_id]:
                stddev += (orig_data[neighbor][time_id] - mean)**2
            stddev = math.sqrt(stddev/N)

            data[district_id][time_id] = [round(mean, 2), round(stddev, 2)]
    
    return data


week_data = load_data("cases-week.csv")
month_data = load_data("cases-month.csv")
overall_data = load_data("cases-overall.csv")


def output_data(data, filename):
    with open(filename, 'a') as f:
        for district_id, y in data.items():
            for time_id, calc in y.items():
                f.write(str(district_id) + "," + str(time_id) + "," + str(calc[0]) + "," + str(calc[1]) + "\n")

output_data(week_data, "neighbor-week.csv")
output_data(month_data, "neighbor-month.csv")
output_data(overall_data, "neighbor-overall.csv")