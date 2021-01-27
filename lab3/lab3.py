import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from collections import Counter

dataset_length = 94
data_list = []

with open("bank.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader, None)
    for lines in csv_reader:
      if len(data_list) < 94:
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

k = 1 + math.floor(3.322*math.log(dataset_length,10))

x_max = data_list[dataset_length-1]
x_min = data_list[0]

h = round(((x_max-x_min)/k),1)
print(h)

x_0 = x_min
x_z = x_0

interval_dict_absolute = {}
interval_dict_relative = {}

int_list = []
solo_list = []

for elem in range(0,k):
    counter = 0
    x_top = round((x_0 + h),2)
    temp_list = [x_0, x_top]
    solo_list.append(x_0)
    #interval_dict[temp_list] = 0

    for i in range(0, len(data_list)):
        if data_list[i] < x_top and data_list[i] >= x_0:
            counter = counter + 1
    
    interval_dict_absolute[str(temp_list)] = counter
    interval_dict_relative[str(temp_list)] = counter/dataset_length

    int_list.append(temp_list)

    x_0 = x_top

solo_list.append(x_top)

print('\nИнтервальный ряд абсолютных частот:\n')
print(interval_dict_absolute)

print('\nИнтервальный ряд относительных частот:\n')
print(interval_dict_relative)

#print(int_list)
mid_list = []
mid_dict = {}
for i in range(0,len(int_list)):
    mid_list.append((int_list[i][0]+int_list[i][1])/2)
    mid_dict[str(int_list[i])] =round(((int_list[i][0]+int_list[i][1])/2),2)

cum_sum = 0
rel_sum = 0

print('\n')
for key, value in interval_dict_absolute.items():
    cum_sum+=value
    print('Для интервала ', key, ' накопленная частота равна: ', cum_sum)

print('\n')
for key, value in interval_dict_relative.items():
    rel_sum+=value
    print('Для интервала ', key, ' накопленная частота равна: ', rel_sum)

print('\n')
for key, value in mid_dict.items():
    print('Для интервала ', key, ' среднее значение равно: ', value)

#Расчет выборочного среднего
com_avg = 0
for key, value in mid_dict.items():
    com_avg+=round(value,2)*interval_dict_absolute[key]
com_avg = round((com_avg/dataset_length),3)

#Расчет выборочной дисперсии
var_sum = 0
for key, value in mid_dict.items():
    var_sum+=(pow((value-com_avg),2)*interval_dict_absolute[key])
s_squared = round(((1/(dataset_length-1))*var_sum),3)
print('s_squared - ', s_squared)
s = round(math.sqrt(s_squared),3)
print('s - ', s)

#Коэффициент Стьюдента при надежности 0.95
koef_Stud = 1.99

#Расчет точности оценки
epsilon = round((koef_Stud*s/math.sqrt(94)),3)
print('eps', epsilon)

#Расчет доверительного интервала
print('\nРасчет доверительного интервала при надежности 0.95:')
print('('+str(com_avg)+'-'+str(epsilon)+','+str(com_avg)+'+'+str(epsilon)+')')
print('ИЛИ')
print('('+str(com_avg-epsilon)+','+str(com_avg+epsilon)+')')

#Коэффициент Стьюдента при надежности 0.99
koef_Stud = 2.64

#Расчет точности оценки
epsilon = round((koef_Stud*s/math.sqrt(94)),3)
print('eps', epsilon)

#Расчет доверительного интервала
print('\nРасчет доверительного интервала при надежности 0.99:')
print('('+str(com_avg)+'-'+str(epsilon)+','+str(com_avg)+'+'+str(epsilon)+')')
print('ИЛИ')
print('('+str(com_avg-epsilon)+','+str(com_avg+epsilon)+')')

#Расчет доверительного интервала СКО
#Коэффициент q для надежности 0.95 и объема выборки 94
q = 0.151
print('\nРасчет доверительного интервала СКО при надежности 0.95:')
left_term = s*(1-q)
right_term = s*(1+q)
print('('+str(s)+'-'+str(round((s*q),3))+','+str(s)+'+'+str(round((s*q),3))+')')
print('ИЛИ')
print('('+str(round((s-s*q),3))+','+str(round((s+s*q),3))+')')

#Расчет доверительного интервала СКО
#Коэффициент q для надежности 0.95 и объема выборки 94
q = 0.211
print('\nРасчет доверительного интервала СКО при надежности 0.99:')
left_term = s*(1-q)
right_term = s*(1+q)
print('('+str(s)+'-'+str(round((s*q),3))+','+str(s)+'+'+str(round((s*q),3))+')')
print('ИЛИ')
print('('+str(round((s-s*q),3))+','+str(round((s+s*q),3))+')')

#Расчет теоретических частот вариант 
theor_freq = []
print('\nРасчет теоретических частот вариант:')
Phi = lambda x: erf(x/2**0.5)/2

for item in range(len(solo_list)-1):
    left_term = (solo_list[item]-com_avg)/s
    right_term = (solo_list[item+1]-com_avg)/s
    result = round(((Phi(left_term) - Phi(right_term))),4) * -1
    print('Для интервала ['+str(solo_list[item])+','+str(solo_list[item+1])+']:')
    print('P_i =', result)
    theor_freq.append(result)

#Расчет выравнивающих частот
viravn_freq = []
for item in range(len(theor_freq)):
    viravn_freq.append(theor_freq[item]*dataset_length)
print('Выравнивающие частоты:', viravn_freq)

#Расчет (m_i - m_i')^2
m_diff_list = []
ind = 0
for key, value in interval_dict_absolute.items():
    res = round((pow((value-viravn_freq[ind]),2)),4)
    m_diff_list.append(res)
    ind+=1
print(m_diff_list)

#Расчет (m_i - m_i')^2/m_i' и наблюдаемого значения согласия Пирсона Х^2
m_final_list = []
x_2_nabl = 0
for item in range(len(viravn_freq)):
    res = round((m_diff_list[item]/viravn_freq[item]),4)
    m_final_list.append(res)
    x_2_nabl+=res
x_2_nabl = round(x_2_nabl,4)
print("\nНаблюдаемое значение согласия Пирсона X^2:", x_2_nabl)

#Сравнение наблюдаемого значения с критическим
x_kp = 9.487
print("Критическое значение согласия Пирсона:", x_kp)

if(x_2_nabl<x_kp):
    print(x_2_nabl, "<", x_kp)
    print("Нет оснований для отвержения гипотезы о нормальности заданного распределения")
else:
    print(x_2_nabl, ">", x_kp)
    print("Гипотеза о нормальности заданного распределения отвергается")
