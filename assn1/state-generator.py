import json
import math

district_ids = json.loads(open("neighbor-districts-modified.json", 'r').read())
state_to_ids = {}
id_to_state = {}
for x in district_ids.keys():
    id = x.split('|')[0]
    state = x.split('|')[2]
    id_to_state[id] = state
    if state not in state_to_ids:
        state_to_ids[state] = []
    state_to_ids[state].append(id)


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
        state = id_to_state[district_id]
        N = len(state_to_ids[state]) - 1
        for time_id in x.keys():
            mean = 0
            for id in state_to_ids[state]:
                if id != district_id:
                    mean += orig_data[id][time_id]
            if N!=0:
                mean /= N

            stddev = 0
            for id in state_to_ids[state]:
                if id != district_id:
                    stddev += (orig_data[id][time_id] - mean)**2
            if N!=0:
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

output_data(week_data, "state-week.csv")
output_data(month_data, "state-month.csv")
output_data(overall_data, "state-overall.csv")