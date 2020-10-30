import json

district_ids = json.loads(open("neighbor-districts-modified.json", 'r').read())

with open("edge-graph.csv", 'a') as f:
    for x, y in district_ids.items():
        for z in y:
            id1 = x.split('|')[0]
            id2 = z.split('|')[0]
            f.write(id1 + "," + id2 + "\n")
