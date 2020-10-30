import requests
import json
import os

ans = {}
if not os.path.exists("data.json"):
    for i in range(1, 16):
        filename = "data" + str(i) + ".json"
        if not os.path.exists(filename):
            url = "https://api.covid19india.org/raw_data"+str(i)+".json"
            r = requests.get(url)
            open(filename, "wb").write(r.content)
        
        data = open(filename, 'r').read()
        data_list = json.loads(data)["raw_data"]
        
        for y in data_list:
            district = y["detecteddistrict"]
            state = y["detectedstate"]
            date = y["dateannounced"]
            cases = y["numcases"]
            status = y["currentstatus"]

            restricted_cases = ["", "0"]
            restricted_districts = ["", "unknown", "unassigned", "airport_quarantine", "bsf_camp", "capf_personnel", "evacuees", "foreign_evacuees", "italians", "other_region", "other_state", "others", "railway_quarantine", "state_pool"]
            district = district.lower().replace(" ", "_")

            if status.lower() == "hospitalized":
                if state.lower() == "delhi" and cases not in restricted_cases:
                    district_state = "delhi|delhi"
                    cases = int(cases)
                    if date not in ans:
                        ans[date] = {}
                    if district_state not in ans[date]:
                        ans[date][district_state] = cases
                    else:
                        ans[date][district_state] += cases

                elif district not in restricted_districts and cases not in restricted_cases:
                    district_state = district + "|" + state.lower().replace(" ", "_")
                    cases = int(cases)

                    if date not in ans:
                        ans[date] = {}
                    if district_state not in ans[date]:
                        ans[date][district_state] = cases
                    else:
                        ans[date][district_state] += cases


    for date in ans.keys():
        negative_cases = []
        for district in ans[date].keys():
            if ans[date][district] <= 0:
                negative_cases.append(district)
        for district in negative_cases:
            ans[date].pop(district)

    with open("data.json", 'w') as f:
        f.write(json.dumps(ans, indent=4))

ans = json.loads(open("data.json", 'r').read())    
states = {}
for date in ans.keys():
    for district_state in ans[date].keys():
        state = district_state.split('|')[1]
        district = district_state.split('|')[0]
        if state not in states:
            states[state] = {}
        if district not in states[state]:
            states[state][district] = 1

state_district = {}
for state in states:
    district_list = list(states[state].keys())
    district_list.sort()
    state_district[state] = district_list

with open("states.json", 'w') as f:
    f.write(json.dumps(state_district, indent=4, sort_keys=True))