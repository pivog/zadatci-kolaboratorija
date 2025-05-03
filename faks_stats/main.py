import numpy
#from numpy.random import random
import pandas as pd
import csv
import matplotlib.pyplot as plt

csv_read = pd.read_csv("data.csv")

columns = []
countries_names = []
data_dicts = []

# Extract data from tetriary school enrolment into python objects
with open('data.csv', "r") as file:
    plots = csv.reader(file, delimiter=',')
    rows = []
    for row in plots:
        rows.append(row)
    
    columns = rows[0]

    out = 0
    for row in rows[1:]:
        if row[1] != "SE.TER.ENRR":
            out += 1
            continue
        if row[3] == "ZWE":
            break
        dic = {}
        for i in range(len(columns)):
            dic[columns[i]] = row[i]
        data_dicts.append(dic)


def get_data_for_year(year:int):
    out = []
    for point in data_dicts:
        try:
            out.append(float(point[f"{year} [YR{year}]"]))
        except: pass
    return out

def mean(points):
    return sum(points)/len(points)

def std_dev(points):
    return numpy.sqrt(sum([pow(x-mean(points), 2) for x in points])/(len(points)))

def skewness(points):
    res = (len(points)/(len(points)-2))*(sum([pow(x-mean(points), 3) for x in points])/((len(points)-1)*pow(std_dev(data_points), 3)))
    return res

def median(points):
    if len(points)%2:
        return points[len(points)/2-1]
    else:
        return mean((points[int(len(points)/2)], points[int(len(points)/2+1)]))

def percentile_binary_search(points, point):
    index = int(len(points)/2)
    upper = len(points)-1
    lower = 0
    while index not in [upper, lower]:
        if points[index]==point:
            break
        if points[index]>point:
            upper = index
            index = int((upper-lower)/2+lower)
        else:
            lower = index
            index = int((upper-lower)/2+lower)
    return index/len(points)*100, index

def z_index(points, point):
    return (point-mean(points))/std_dev(points)

data_points = get_data_for_year(2023)
data_points = sorted(data_points)
avg = mean(data_points)
bh = 0
for c in data_dicts:
    if c["Country Code"] == "BIH":
        bh = float(c["2023 [YR2023]"])

print('Opis distribucije')
print('Aritmeticka sredina: ' + str(avg))
print('Standardna devijacija: '+str(std_dev(data_points)))
print('Skjunis: '+str(skewness(data_points)))
print('Medijana: '+str(median(data_points)))
print("------------------------")
print('Podatak za BiH')
print('Vrijednost: '+str(bh)+'%')
print('z-indeks: '+str(z_index(data_points, bh)))
print('Centil: '+str(percentile_binary_search(data_points, bh)[0]))

plt.hist(data_points, color="g", label="Postotak upisa u višu školu", bins=[i for i in range(0, 160, 10)])
#plt.scatter(data_points, [random()+17 for x in range(len(data_points))])

# Vertical line for BH

line_pt1, line_pt2 = numpy.array([bh, bh]), numpy.array([0, 12])
plt.plot(line_pt1, line_pt2, c="red", linewidth=4, label="Bosna i Hercegovina")
plt.legend(loc="best")
plt.show()
