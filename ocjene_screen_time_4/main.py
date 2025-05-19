from sys import exc_info
import pandas as pd
import matplotlib.pyplot as plt
import csv

from pandas.core.indexes.category import contains

columns = []
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
        if row[9] not in [str(x) for x in range(1, 5)]:
            out += 1
            continue
        dic = {}
        for i in range(len(columns)):
            dic[columns[i]] = row[i]
        data_dicts.append(dic)

print(columns)
print(data_dicts[1])

days = {}
for day in columns[1:8]:
    days[day]=0

print(days.keys())

def to_hours(unf):
    print(unf)
    try:
        if len(unf.split()) == 1:
            return int(unf.split()[0])
        if len(unf.split()) == 2:
            return int(unf.split()[0]) + float(unf.split()[1])/60
    except Exception as e:
        print(e)
        return -1
    return -1


for day in days.keys():
    divisor = 0
    for person in data_dicts:
        time_unformatted = person[day]
        try:
            time = -1
            if len(time_unformatted.split())==1:
                time = int(time_unformatted.split()[0])
            elif len(time_unformatted.split())==2:
                time = int(time_unformatted.split()[0])+float(time_unformatted.split()[1])
            days[day]+=time
        except:
            pass

def float_or_zero(f):
    try:
        return float(f)
    except:
        return 0

def get_person_avg(p):
    divisor = 0
    sum = 0
    for day in days.keys():
        if not p[day]:
            continue
        sum += to_hours(p[day])
        divisor += 1
    if divisor == 0:
        return -1
    return sum/divisor


scatter_plot = plt.scatter([get_person_avg(p) for p in data_dicts], [float_or_zero(p["gpa"]) for p in data_dicts])
plt.xlabel("Prosječno Vrijeme Provedeno na Mobitelu")
plt.ylabel("Prosjek Ocjena u Trenutku Ispitivanja")
l, r = plt.xlim()
plt.xlim(0, r)
u, d = plt.ylim()
plt.ylim(0.8, d)
print([float_or_zero(p["mon"]) for p in data_dicts])

plt.show()
