#!/usr/bin/python3

import csv
import matplotlib.pyplot as plt
from scipy import stats

data_set = ["data-2018.csv", "data-2019.csv" ,"data-2020.csv", "data-2021.csv"]

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

def join(cisla, vzdalenosti):
    ret = {}
    for x, y in cisla.items():
        if x in vzdalenosti.keys():
            ret[x] = (vzdalenosti[x], y)
    return ret

def values(cisla):
    x_axe = []
    y_axe = []

    for x, y in cisla.items():
        print(x, y)
        x_axe.append(y[0])
        y_axe.append(y[1])
    return x_axe, y_axe


def prepare(f): 
    data = []

    with open(f) as csv_file:
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

def process(f):
    cisla = prepare(f)
    vzdalenosti = match_distance()

    cisla = join(cisla, vzdalenosti)
    return cisla

x_axe = []
y_axe = []

for x in data_set:
    x2_axe, y2_axe = values(process(x))
    x_axe += x2_axe
    y_axe += y2_axe



slope, intercept, r, p, std_err = stats.linregress(x_axe, y_axe)


print("p-value = {0} \n r-value = {1}".format(p, r))

def line(x):
  return slope * x + intercept

mymodel = list(map(line, x_axe))


plt.scatter(x_axe, y_axe)
plt.plot(x_axe, mymodel)
plt.xlabel('vzdálenost od středu Prahy v mílích')
plt.ylabel('počet nehod')


plt.savefig('linear.png')
plt.show()
