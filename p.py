#!/usr/bin/python3

import csv
import matplotlib.pyplot as plt
from scipy import stats

def match_distance():
    with open('vzdalenosti.csv') as csv_file:
        data = {}
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            x = row[0].upper() 
            y = row[1]
            if len(x) > 0 and len(y) > 0: 
                data[x] = float(y)
        return data



def prepare(): 
    data = []

    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                x = row[3].upper()
                if len(x) > 0: 
                    data.append(x)

    d = {}

    for x in data:
        if not x in d.keys():
            d[x] = 0
        d[x] += 1

    data = {}

    for x,y in d.items():
        if y >= 1000:
            data[x] = y

    return data


cisla = prepare()
vzdalenosti = match_distance()

for x, y in cisla.items():
    cisla[x] = (vzdalenosti[x], y)

x_axe = []
y_axe = []

for x, y in cisla.items():
    x_axe.append(y[0])
    y_axe.append(y[1])

slope, intercept, r, p, std_err = stats.linregress(x_axe, y_axe)

print(r, p)

def line(x):
  return slope * x + intercept

mymodel = list(map(line, x_axe))


plt.scatter(x_axe, y_axe)
plt.plot(x_axe, mymodel)
plt.xlabel('vzdálenost od středu Prahy v mílích')
plt.ylabel('počet nehod')


plt.savefig('linear.png')
plt.show()
