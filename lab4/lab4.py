import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

dataset_length = 94
data_list = []

vec1 = []
with open("bank.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader, None)
    for lines in csv_reader:
      if len(data_list) < 94:
          data_list.append(int(lines[9]))
          vec1.append(int(lines[0]))

arr1 = np.array(vec1)
arr2 = np.array(data_list)

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
        if data_list[i] <= x_top and data_list[i] > x_0:
            counter = counter + 1
    

    if elem == 0:
        counter+=1
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
    mid_dict[str(int_list[i])] =(int_list[i][0]+int_list[i][1])/2

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

#условные варианты
C = mid_list[int(len(mid_list)/2)]

usl_var_list = []
var_usl_dict = {}

for elem in mid_list:
    usl_var_list.append(round((elem-C)/h))
    var_usl_dict[elem] = (round((elem-C)/h))

print('\nУсловные варианты:')
print(usl_var_list)
print(var_usl_dict)

print('\n С = ' + str(C))

ind = 0
for key, value in interval_dict_relative.items():
    print('Для условной варианты ' + str(usl_var_list[ind]) + ' частота равна: ' + str(value))
    ind+=1

#Получение значений для расчета условных эмпирических моментов
int_ind = 0
sum_for_emp = [0,0,0,0]
print('Получение значений для расчета условных эмпирических моментов:')
for key, value in interval_dict_absolute.items():
    uvar = usl_var_list[int_ind]
    print(key,value,uvar, value*uvar, value*pow(uvar,2), value*pow(uvar,3), value*pow(uvar,4))
    for i in range(4):
        sum_for_emp[i] += value*pow(uvar,i+1)
    int_ind+=1

#print(sum_for_emp)

#Расчет условных эмп моментов
print('Условные эмпирические моменты:')
for i in range(len(sum_for_emp)):
    sum_for_emp[i] = round((sum_for_emp[i]/dataset_length), 3)
    print('M'+str(i+1),': ', sum_for_emp[i])

m1_emp = sum_for_emp[0]
m2_emp = sum_for_emp[1]
m3_emp = sum_for_emp[2]
m4_emp = sum_for_emp[3]

#Расчет центральных эмп моментов
print('Центральные эмпирические моменты:')
u2_emp = round(((m2_emp-pow(m1_emp,2))*pow(h,2)),3)
u3_emp = round(((m3_emp-3*m1_emp*m2_emp+2*pow(m1_emp,3))*pow(h,3)),3)
u4_emp = round(((m4_emp-4*m1_emp*m3_emp+6*m2_emp*pow(m1_emp,2)-3*pow(m1_emp,4))*pow(h,4)),3)
print(u2_emp)
print(u3_emp)
print(u4_emp)

#Расчет выборочного среднего по формуле
com_avg = 0
for key, value in mid_dict.items():
    com_avg+=round(value,2)*interval_dict_absolute[key]
com_avg = com_avg/dataset_length
print('Расчет выборочного среднего по формуле: ' , round(com_avg,2))

#Расчет мат.ожидания
mat_oj = 0
for key, value in var_dict.items():
    mat_oj+=key*value/dataset_length
mat_oj=round(mat_oj, 3)
print('Расчет математического ожидания: ', mat_oj)
#Расчет дисперсии по формуле 
var_1 = 0
var_2 = 0
for key, value in mid_dict.items():
    var_1+=round(pow(value,2),2)*interval_dict_relative[key]
    var_2+=round(value,2)*interval_dict_relative[key]
var_2 = pow(var_2, 2)
total_var = var_1 - var_2
print("Расчет дисперсии по формуле: ", round(total_var,1))

#Расчет СКО
kv_otkl = round(math.sqrt(total_var),3)
print('СКО: ', kv_otkl)
#Расчет выборочного среднего с помощью условных вариант 
com_avg = m1_emp*h+C
print('Расчет выборочного среднего с помощью условных вариант: ' , round(com_avg,2))

#Расчет дисперсии с помощью условных вариант 
print('Расчет дисперсии с помощью условных вариант: ',round(u2_emp,1))

#Расчет коэффициентов асимметрии и эксцесса
asym_koef = u3_emp/pow(kv_otkl,3)
exc_koef = u4_emp/pow(kv_otkl,4) - 3
print('Коэффициент асимметрии: ', asym_koef)
print('Коэффициент эксцесса: ', exc_koef)

#Расчет моды
top_value = 0
left_value = 0
right_value = 0
freq_list = []
for key, value in interval_dict_absolute.items():
    freq_list.append(value)
for i in range(len(freq_list)):
    if freq_list[i] > top_value:
        top_value = freq_list[i]
        if i == 0:
            left_value = 0
        else:
            left_value = freq_list[i-1]
        if i == len(freq_list):
            right_value = 0
        else:
            right_value = freq_list[i+1]
for key, value in interval_dict_absolute.items():
    if value == top_value:
        x_0 = float(key[1:5])

moda = x_0 + h*((top_value-left_value)/((top_value-left_value)+(top_value-right_value)))

print('Мода: ', round(moda,2))

#Расчет медианы
med_interval = []
cum_sum = 0
prev_cum_sum = 0
freq = 0
for key, value in interval_dict_absolute.items():
    cum_sum+=value
    if cum_sum >= dataset_length/2:
        med_interval = key
        freq = value
        break
    prev_cum_sum = cum_sum

int_begin = float(med_interval[1:5])
int_end = float(med_interval[7:11])

mi_sum = 0
for key, value in interval_dict_absolute.items():
    mi_sum += value
median = int_begin+(h/freq)*(0.5*mi_sum-prev_cum_sum)

print("Медиана: ", round(median,2))

#Расчет коэфф вариации
koef_var = (kv_otkl/com_avg)*100
print("Коэффициент вариации: ", round(koef_var,2), "%")

#Таблица двумерного интервального вариационного ряда
k = 1 + math.floor(3.322*math.log(dataset_length,10))

vec1.sort()

x_max = vec1[dataset_length-1]
x_min = vec1[0]

h = round(((x_max-x_min)/k),1)

x_0 = x_min
x_z = x_0

int_list2 = []
solo_list = []

for elem in range(0,k):
    counter = 0
    x_top = round((x_0 + h),2)
    temp_list = [x_0, x_top]
    solo_list.append(x_0)

    int_list2.append(temp_list)

    x_0 = x_top

solo_list.append(x_top)


corr_dict = {}
ind = 0
for i in arr1:
    if i not in corr_dict:
        corr_dict[i] = list()
        corr_dict[i].append(arr2[ind])
    else:
        corr_dict[i].append(arr2[ind])
    ind+=1

keylist = sorted(corr_dict.keys())

matrix = np.zeros((7,7))

for key, value in corr_dict.items():
    for i in range(7):
        if ((key > int_list2[i][0] and key <= int_list2[i][1])) or (i == 0 and key >= int_list2[i][0] and key <= int_list2[i][1]):
            y_pos = i
    for j in range(7):
        for item in value:
            if ((item > int_list[j][0] and item <= int_list[j][1])) or j == 0 and (item >= int_list[j][0] and item <= int_list[j][1]):
                x_pos = j
                matrix[y_pos][x_pos]+=1
            
matrix[0][0]
print("\nТаблица двумерного интервального ряда:")
print(matrix)

#Корелляционная таблица
mid_age = []
for i in range(len(int_list2)):
    mid_age.append(round((((int_list2[i][0]+int_list2[i][1])/2)),2))
print(mid_age)

mid_day_of_hire = []
for i in range(len(int_list)):
    mid_day_of_hire.append(round((((int_list[i][0]+int_list[i][1])/2)),2))
print(mid_day_of_hire)

#Статистическая оценка корреляционного момента
cor_sum = 0
for i in range(7):
    for j in range(7):
        cor_sum+=matrix[i][j]*(mid_age[i]-41.66)*(mid_day_of_hire[j]-15.12)

stat_cor = cor_sum/dataset_length
print("Статистическая оценка корреляционного момента: ", round(stat_cor,3))
sko_fixed = round(math.sqrt(total_var*dataset_length/(dataset_length-1)),2)
sko_age_fixed = 11.1
r = round((stat_cor/(sko_age_fixed*sko_fixed)),3)
print("Коэффициент корреляции: ", r)

#Доверительный интервал при точности 0.95
print('\nДоверительный интервал при точности 0.95:')
left_side = math.tanh(math.atanh(r)-(1.95996635682/math.sqrt(dataset_length-3)))
right_side = math.tanh(math.atanh(r)+(1.95996635682/math.sqrt(dataset_length-3)))

print('('+str(round(left_side,3))+','+str(round(right_side,3))+')')

#Доверительный интервал при точности 0.99
print('\nДоверительный интервал при точности 0.99:')
left_side = math.tanh(math.atanh(r)-(2.57583422011/math.sqrt(dataset_length-3)))
right_side = math.tanh(math.atanh(r)+(2.57583422011/math.sqrt(dataset_length-3)))

print('('+str(round(left_side,3))+','+str(round(right_side,3))+')')

#Нулевая гипотеза
T_nabl = r*math.sqrt(dataset_length-2)/math.sqrt(1-pow(r,2))
print(T_nabl)

T_krit = 1.95996635682

if(abs(T_nabl) < abs(T_krit)):
    print('|'+str(T_nabl)+'|', "<",'|'+ str(T_krit)+ '|')
    print("Нет оснований для отвержения нулевой гипотезы")
else:
    print('|'+str(T_nabl)+'|', ">",'|'+ str(T_krit)+ '|')
    print("Есть основания для отвержения нулевой гипотезы")