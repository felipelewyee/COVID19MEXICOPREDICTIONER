import numpy as np

dates = np.arange('2020-01-22', '2020-04-09', dtype='datetime64[D]')
print(dates)

f = open('database_confirmed.csv','r')

for line in f:
    pais = line.split(',')[0]
    dias = line.split(',')[1:]
    for i,dia in enumerate(dias):
        if (int(dia)!=0):
            print(pais+','+str(dates[i]))
            break

