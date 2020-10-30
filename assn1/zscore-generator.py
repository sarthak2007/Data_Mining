import json

def output_data(orig_file, neighbor_file, state_file, output_file):
    with open(orig_file, 'r') as f:
        list1 = f.readlines()

    with open(neighbor_file, 'r') as f:
        list2 = f.readlines()

    with open(state_file, 'r') as f:
        list3 = f.readlines()
    
    output_f = open(output_file, 'a')
    for i in range(len(list1)):
        district_id = list1[i].split(',')[0]
        time_id = list1[i].split(',')[1]
        cases = int(list1[i].split(',')[2][:-1])
        mean1 = float(list2[i].split(',')[2])
        mean2 = float(list3[i].split(',')[2])
        stddev1 = float(list2[i].split(',')[3][:-1])
        stddev2 = float(list3[i].split(',')[3][:-1])

        zscore1, zscore2 = 0, 0

        if stddev1 != 0:
            zscore1 = (cases - mean1)/stddev1
        if stddev2 != 0:
            zscore2 = (cases - mean2)/stddev2
        
        zscore1 = round(zscore1, 2)
        zscore2 = round(zscore2, 2)

        output_f.write(district_id + "," + time_id + "," + str(zscore1) + "," + str(zscore2) + "\n")
    
    output_f.close()

output_data("cases-week.csv", "neighbor-week.csv", "state-week.csv", "zscore-week.csv")
output_data("cases-month.csv", "neighbor-month.csv", "state-month.csv", "zscore-month.csv")
output_data("cases-overall.csv", "neighbor-overall.csv", "state-overall.csv", "zscore-overall.csv")