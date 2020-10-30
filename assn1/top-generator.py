import json

def load_data(filename):
    data = {}
    with open(filename, 'r') as f:
        elem = f.readlines()
        for temp in elem:
            district_id = temp.split(',')[0]
            time_id = temp.split(',')[1]
            neighbor_zscore = float(temp.split(',')[2])
            state_zscore = float(temp.split(',')[3][:-1])

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

            if neighbor_zscore > 1:
                data[time_id]["neighborhood"]["hot"].append((district_id, neighbor_zscore))
            elif neighbor_zscore < -1:
                data[time_id]["neighborhood"]["cold"].append((district_id, neighbor_zscore))

            if state_zscore > 1:
                data[time_id]["state"]["hot"].append((district_id, state_zscore))
            elif state_zscore < -1:
                data[time_id]["state"]["cold"].append((district_id, state_zscore))
    
    return data


week_data = load_data("zscore-week.csv")
month_data = load_data("zscore-month.csv")
overall_data = load_data("zscore-overall.csv")


def output_data(data, filename):
    with open(filename, 'a') as f:
        for time_id, y in data.items():
            for method, x in y.items():
                for spot, district_ids in x.items():
                    if spot == "hot":
                        district_ids.sort(key = lambda x : x[1], reverse = True)
                    else:
                        district_ids.sort(key = lambda x : x[1])
                        
                    f.write(time_id + "," + method + "," + spot)
                    for i in range(min(len(district_ids), 5)):
                        f.write("," + district_ids[i][0])
                    for i in range(max(5-len(district_ids), 0)):
                        f.write(",NA")
                    f.write("\n")
                    

output_data(week_data, "top-week.csv")
output_data(month_data, "top-month.csv")
output_data(overall_data, "top-overall.csv")