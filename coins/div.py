csvfile = open('../data/input_data.csv', 'r').readlines()
filename = 1
for i in range(len(csvfile)):
    if i % 30 == 0:
        open("../data/" + str(filename) + '.csv', 'w+').writelines(csvfile[i:i+30])
        filename += 1
