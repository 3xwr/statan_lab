import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def show_graphs(relative_bool=False):
#Полигон частот
    if relative_bool:
        text = " относительных "
    else:
        text = " абсолютных "
    y,edges = np.histogram(data_list, boundaries, density=relative_bool) #  note only two arguments, _ missing
    centers = 0.5*(edges[1:]+ edges[:-1])

    plt.plot(centers,y,'-*')      # other options '--'  '-^'
    plt.title('Полигон' + text + 'частот')
    plt.show()

    #Гистограмма 

    y = np.array(boundaries)
    x = np.array(data_list)

    plt.hist(x, y, facecolor='blue', alpha=0.5, histtype='bar', ec='black', density=relative_bool)
    plt.title('Гистограмма' + text + 'частот')
    plt.show()

    #Эмпирическая функция 

    plt.hist(x, y, facecolor='blue', alpha=0.5, histtype='bar', ec='black', density=1, cumulative=True)
    plt.title('Эмпирическая функция' + text + 'частот')
    plt.show()

    #Кумулята

    y,edges = np.histogram(data_list, boundaries, density=relative_bool) #  note only two arguments, _ missing
    centers = 0.5*(edges[1:]+ edges[:-1])
    cum = np.cumsum(y)
    plt.plot(centers,cum,'-*')      # other options '--'  '-^'
    plt.title('Кумулята'+ text + 'частот')
    plt.show()

dataset_length = 91
data_list = []

with open("bank.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader, None)
    for lines in csv_reader:
      if len(data_list) < 91:
          print(lines[0])
          data_list.append(int(lines[0]))

print('\nИсходный набор данных:\n')
print(data_list)

data_list.sort()
print('\nРанжированный ряд:\n')
print(data_list)

print('\nВариационный ряд:\n')
var_dict = dict(Counter(data_list))
print(var_dict)

k = 1 + math.floor(math.log(dataset_length,2))

x_max = data_list[dataset_length-1]
x_min = data_list[0]

h = (x_max-x_min)/k
h = int(h)

x_0 = x_min - int(h/2)
x_z = x_0

interval_dict_absolute = {}
interval_dict_relative = {}

int_list = []

for elem in range(0,k):
    counter = 0
    x_top = x_0 + h
    temp_list = [x_0, x_top]

    #interval_dict[temp_list] = 0

    for i in range(0, len(data_list)):
        if data_list[i] < x_top and data_list[i] >= x_0:
            counter = counter + 1
    
    interval_dict_absolute[str(temp_list)] = counter
    interval_dict_relative[str(temp_list)] = counter/dataset_length

    int_list.append(temp_list)

    x_0 = x_top

print('\nИнтервальный ряд абсолютных частот:\n')
print(interval_dict_absolute)

print('\nИнтервальный ряд относительных частот:\n')
print(interval_dict_relative)


boundaries = []
x_bot = x_z
for elem in range(0,k+1):
    x_top = x_bot+h

    boundaries.append(x_bot)
    
    x_bot = x_top

show_graphs()
show_graphs(True)