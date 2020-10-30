import json
from datetime import date, timedelta

start_date = date(2020, 3, 15)
end_date = date(2020, 9, 5)
delta = timedelta(days=1)

district_ids = json.loads(open("neighbor-districts-modified.json", 'r').read())
id_to_district = {}
district_to_id = {}
for x in district_ids.keys():
    id = x.split('|')[0]
    district = "|".join(x.split('|')[1:3])
    id_to_district[id] = district
    district_to_id[district] = id

data = json.loads(open("data.json", 'r').read())
week_data, month_data, overall_data = {}, {}, {}
cnt = 7

def fill_data(district_id, time_id, data, fill_data, date):
    if district_id not in fill_data:
        fill_data[district_id] = {}
    if time_id not in fill_data[district_id]:
        fill_data[district_id][time_id] = 0
    
    district_name = id_to_district[str(district_id)]
    if date in data and district_name in data[date]:
        fill_data[district_id][time_id] += data[date][district_name]

while start_date <= end_date:
    date = start_date.strftime("%d/%m/%Y")
    week_id = cnt//7
    month_id = start_date.month - 2
    overall_id = 1

    for district_id in range(101, 811):
        fill_data(district_id, week_id, data, week_data, date)
        fill_data(district_id, month_id, data, month_data, date)
        fill_data(district_id, overall_id, data, overall_data, date)

    cnt += 1
    start_date += delta    


def output_data(data, filename):
    with open(filename, 'a') as f:
        for district_id, y in data.items():
            for time_id, cases in y.items():
                f.write(str(district_id) + "," + str(time_id) + "," + str(cases) + "\n")

output_data(week_data, "cases-week.csv")
output_data(month_data, "cases-month.csv")
output_data(overall_data, "cases-overall.csv")