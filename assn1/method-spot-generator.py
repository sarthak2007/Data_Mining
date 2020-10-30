import json

def load_data(file1, file2, file3):
    data = {}
    state_data = {}
    neighbor_data = {}
    with open(file2, 'r') as f:
        elem = f.readlines()
        for temp in elem:
            district_id = temp.split(',')[0]
            time_id = temp.split(',')[1]
            mean = float(temp.split(',')[2])
            stddev = float(temp.split(',')[3][:-1])
            if district_id not in neighbor_data:
                neighbor_data[district_id] = {}
            neighbor_data[district_id][time_id] = [mean, stddev]

    with open(file3, 'r') as f:
        elem = f.readlines()
        for temp in elem:
            district_id = temp.split(',')[0]
            time_id = temp.split(',')[1]
            mean = float(temp.split(',')[2])
            stddev = float(temp.split(',')[3][:-1])
            if district_id not in state_data:
                state_data[district_id] = {}
            state_data[district_id][time_id] = [mean, stddev]

    with open(file1, 'r') as f:
        elem = f.readlines()
        for temp in elem:
            district_id = temp.split(',')[0]
            time_id = temp.split(',')[1]
            cases = float(temp.split(',')[2][:-1])

            if time_id not in data:
                data[time_id] = {}

            methods = ["neighborhood", "state"]
            spots = ["cold", "hot"]
            for method in methods:
                if method not in data[time_id]:
                    data[time_id][method] = {}
                for spot in spots:
                    if spot not in data[time_id][method]:
                        data[time_id][method][spot] = []

            if cases > neighbor_data[district_id][time_id][0] + neighbor_data[district_id][time_id][1]:
                data[time_id]["neighborhood"]["hot"].append(district_id)
            elif cases < neighbor_data[district_id][time_id][0] - neighbor_data[district_id][time_id][1]:
                data[time_id]["neighborhood"]["cold"].append(district_id)

            if cases > state_data[district_id][time_id][0] + state_data[district_id][time_id][1]:
                data[time_id]["state"]["hot"].append(district_id)
            elif cases < state_data[district_id][time_id][0] - state_data[district_id][time_id][1]:
                data[time_id]["state"]["cold"].append(district_id)
    
    return data


week_data = load_data("cases-week.csv", "neighbor-week.csv", "state-week.csv")
month_data = load_data("cases-month.csv", "neighbor-month.csv", "state-month.csv")
overall_data = load_data("cases-overall.csv", "neighbor-overall.csv", "state-overall.csv")


def output_data(data, filename):
    with open(filename, 'a') as f:
        for time_id, y in data.items():
            for method, x in y.items():
                for spot, district_ids in x.items():
                    district_ids.sort()
                    for district_id in district_ids:
                        f.write(time_id + "," + method + "," + spot + "," + district_id + "\n")
                    

output_data(week_data, "method-spot-week.csv")
output_data(month_data, "method-spot-month.csv")
output_data(overall_data, "method-spot-overall.csv")