import json

district_mappings = {}

data1 = open("neighbor-districts.json", 'r').read()
data1 = json.loads(data1)
district1 = {}
for y in data1.keys():
    district1[y] = 1

data2 = open("states.json", 'r').read()
data2 = json.loads(data2)
district2 = {}
for x in data2.keys():
    for y in data2[x]:
        if y not in district2:
            district2[y] = []
        district2[y].append(x)


def edit_distance(a, b):
    n = len(a)
    m = len(b)

    dp = [[0 for i in range(m+1)] for j in range(n+1)]

    for j in range(m+1):
        dp[0][j] = j
    for i in range(n+1):
        dp[i][0] = i

    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[n][m]

# compute mappings using edit distance
for district in district1.keys():
    y = district.split("/")[0]
    last = y.split("_")[-1]
    if last == "district":
        y = "_".join(y.split("_")[:-1])
    if y in district2:
        district_mappings[district] = y + "|" + district2[y][0]
    else:
        dist, ans = 1000, ""
        for x in district2.keys():
            edit_dst = edit_distance(x, y)
            if(edit_dst < dist):
                dist = edit_dst
                ans = x
        district_mappings[district] = ans + "|" + district2[ans][0]

# changes the mappings
district_mappings["sahibzada_ajit_singh_nagar/Q2037672"] = "s.a.s._nagar|punjab"
district_mappings["palghat/Q1535742"] = "palakkad|kerala"
district_mappings["kochbihar/Q2728658"] = "cooch_behar|west_bengal"
district_mappings["pashchim_champaran/Q100124"] = "west_champaran|bihar"
district_mappings["muktsar/Q1947359"] = "sri_muktsar_sahib|punjab"
district_mappings["the_dangs/Q1135616"] = "dang|gujarat"
district_mappings["jyotiba_phule_nagar/Q1891677"] = "amroha|uttar_pradesh"
district_mappings["kheri/Q1755447"] = "lakhimpur_kheri|uttar_pradesh"
district_mappings["faizabad/Q1814132"] = "ayodhya|uttar_pradesh"
district_mappings["sant_ravidas_nagar/Q127533"] = "bhadohi|uttar_pradesh"
district_mappings["pashchimi_singhbhum/Q1950527"] = "west_singhbhum|jharkhand"
district_mappings["hugli/Q548518"] = "hooghly|west_bengal"
district_mappings["aizwal/Q1947322"] = "aizawl|mizoram"
district_mappings["sonapur/Q1473957"] = "subarnapur|odisha"
district_mappings["kaimur_(bhabua)/Q77367"] = "kaimur|bihar"
district_mappings["baleshwar/Q2022279"] = "balasore|odisha"
district_mappings["dantewada/Q100211"] = "dakshin_bastar_dantewada|chhattisgarh"
district_mappings["bid/Q814037"] = "beed|maharashtra"
district_mappings["belgaum_district/Q815464"] = "belagavi|karnataka"
district_mappings["shimoga_district/Q2981389"] = "shivamogga|karnataka"
district_mappings["ysr/Q15342"] = "y.s.r._kadapa|andhra_pradesh"
district_mappings["east_karbi_anglong/Q42558"] = "karbi_anglong|assam"
district_mappings["aurangabad/Q592942"] = "aurangabad|maharashtra"
district_mappings["balrampur/Q1948380"] = "balrampur|uttar_pradesh"
district_mappings["bilaspur/Q1478939"] = "bilaspur|himachal_pradesh"
district_mappings["hamirpur/Q2019757"] = "hamirpur|uttar_pradesh"
district_mappings["pratapgarh/Q1473962"] = "pratapgarh|uttar_pradesh"
district_mappings["bijapur_district/Q1727570"] = "vijayapura|karnataka"

district_mappings["mumbai_suburban/Q2085374"] = "mumbai|maharashtra"
district_mappings.pop("konkan_division/Q6268840")

district_mappings["east_delhi/Q107960"] = "delhi|delhi"
district_mappings["shahdara/Q83486"] = "delhi|delhi"
district_mappings["south_east_delhi/Q25553535"] = "delhi|delhi"
district_mappings["central_delhi/Q107941"] = "delhi|delhi"
district_mappings["west_delhi/Q549807"] = "delhi|delhi"
district_mappings["north_east_delhi/Q429329"] = "delhi|delhi"
district_mappings["north_west_delhi/Q766125"] = "delhi|delhi"
district_mappings["north_delhi/Q693367"] = "delhi|delhi"
district_mappings["south_west_delhi/Q2379189"] = "delhi|delhi"
district_mappings["south_delhi/Q2061938"] = "delhi|delhi"
district_mappings["new_delhi/Q987"] = "delhi|delhi"

district_mappings["noklak/Q48731903"] = "tuensang|nagaland"

# make the modified neighbor file
neighbors = {}
for x, y in data1.items():
    if x in district_mappings:
        key = district_mappings[x]
        val = []
        for dist in y:
            if dist in district_mappings and district_mappings[dist] not in val and district_mappings[dist] != key:
                val.append(district_mappings[dist])
        if key not in neighbors:
            neighbors[key] = val
        else:
            for dist in val:
                if dist not in neighbors[key]:
                    neighbors[key].append(dist)

district_to_qid = {}
for x, y in district_mappings.items():
    district_to_qid[y] = x.split('/')[1]

qid_to_district = {}
for x, y in district_to_qid.items():
    qid_to_district[x.split('|')[0] + "/" + y] = x

district_to_new_ids = {}
districts = list(qid_to_district.keys())
districts.sort()
id = 101
for dist in districts:
    district_to_new_ids[qid_to_district[dist]] = str(id)
    id += 1

neighbors_with_ids = {}
for x, y in neighbors.items():
    val = []
    for dist in y:
        val.append(district_to_new_ids[dist] + "|" + dist)
    val.sort()
    neighbors_with_ids[district_to_new_ids[x] + "|" + x] = val

with open("neighbor-districts-modified.json", 'w') as f:
    f.write(json.dumps(neighbors_with_ids, indent=4, sort_keys=True))