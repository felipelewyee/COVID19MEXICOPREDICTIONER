#!/usr/bin/env python
# coding: utf-8

# # Red para COVID-19

# Esta es una red secuencial simple para tratar de predecir el dato de número de contagiados de COVID19 en México que se da a las 19:00 horas por parte del gobierno.
# 
# **Para ejecutar la predicción:**
# 
# **1)** Ejecutar processing.sh, este script descarga el archivo time_series_covid19_confirmed_global.csv con datos de contagiados por país. Este archivo se actualiza en internet aproximadamente a las 6:30pm con datos del día anterior, hay que revisar que esté actualizado a la fecha del día de la predicción.
# 
# chmod +x processing.sh
# 
# ./processing.sh
# 
# **2)** Abrir jupyter notebook (se requiere keras, tensorflow, pandas y numpy instaldos).
# 
# jupyter notebook COVID-19.ipynb
# 
# **3)** Actualizar dias_a_usar y dia_a_predecir. Como referencia, el 30 de marzo fue el día 33 de infección en México, por lo que dia_a_predecir=33 y dias_a_usar=32.
# 
# **4)** Ejecutar todos los cuadros.
# 
# **Creado por Juan Felipe Huan Lew Yee, Neftalí Isaí Rodríguez Rojas y Jorge Martín del Campo Ramírez.**

# Definimos el dia que queremos la prediccion

import numpy as np
import keras
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense,Dropout

N = int(input("Cuanto vale la N? "))
repeticiones = int(input("Cuantas repeticiones quiere? "))
dia_inicio_Mexico = 37
predicciones_por_dia = []
valores_por_dia = []
for dia_a_predecir in range(N+1,46):
    predicciones = []
    for i in range(repeticiones):

# In[1]:

        dias_a_usar = dia_a_predecir-N       


# Definimos la lista de paises que analizaremos. (Más abajo se filtrarán los que no tengan suficientes días)

# In[2]:


        country_namelist = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Andorra', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea South', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Maldives', 'Malta', 'Mauritania', 'Mauritius', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tanzania', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'US', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zambia', 'Zimbabwe', 'Dominica', 'Grenada', 'Mozambique', 'Syria', 'Timor-Leste', 'Belize', 'Laos', 'Libya', 'Guinea-Bissau', 'Mali', 'Saint Kitts and Nevis', 'Burma', 'Botswana', 'Burundi', 'Sierra Leone', 'Malawi']


# Filtramos los países que no tengan el número de días necesarios para predecir a México, los países a usar al menos deben de tener dia_a_predecir días de infección.

# In[3]:


        db = open('database.csv','w')
    
        for value in range(dias_a_usar):
            print(value+1,file=db,end = ',')
        print(dia_a_predecir,file=db)

        for country in country_namelist:
    
            f = open('database_confirmed.csv')
            infected = []
            dia_inicio = 0
            for line in f:
                if(country == line.split(',')[1]):
                    country_data = []
                    data = line.replace('\n','').split(',')[4:]
                    for number in data:
                        if(number != '0'):
                            infected.append(int(number))
                        else:
                            dia_inicio += 1                    
            f.close()

            if(len(infected)<=dia_a_predecir):
                #print(country,len(infected))
                continue
            print(country,end=',',file=db,sep=',')
            for value in infected[:dias_a_usar]:
                print(value,file=db,end = ',')
            print(infected[dia_a_predecir-1],file=db)
        db.close()          


# Leamos la base de datos que acabamos de crear.

# In[5]:

    
        data = pd.read_csv("database.csv",sep=',') 


# Imprimimos la base de datos

# In[6]:


        data


# Creamos un conjunto X y un conjunto Y y dividimos train y test

# In[7]:


        X = pd.DataFrame()
        for i in range(1,dias_a_usar+1):
            X[str(i)] = data[str(i)]
        Y = pd.DataFrame()
        Y[str(dia_a_predecir)] = data[str(dia_a_predecir)]
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.05)
        print(X_train.shape, y_train.shape)
        print(X_test.shape, y_test.shape)


# Creamos la red neuronal

# In[8]:


        model = Sequential()
        model.add(Dense(64, input_dim=dias_a_usar+0, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1, activation='linear'))

# Compilamos la red

# In[9]:


        model.compile(loss='MAPE', optimizer='adam')


# Entrenamos la red

# In[10]:


        history = model.fit(X_train, y_train, epochs=1500, validation_data=(X_test,y_test))


# In[11]:


# Plot training & validation loss values (Descomentar para visualizar graficas)
#        plt.plot(history.history['loss'])
#        plt.plot(history.history['val_loss'])
#        plt.title('Model loss')
#        plt.ylabel('Loss')
#        plt.xlabel('Epoch')
#        plt.legend(['Train', 'Test'], loc='upper left')
#        plt.show()


# Realizamos predicciones del test

# In[12]:


        model.predict(X_test)


# Comprobamos

# In[13]:


        y_test


# # Predicción

# In[14]:


        country_prediction_namelist = ['Mexico']


# In[15]:


        db = open('database_prediction.csv','w')

        for value in range(dias_a_usar):
            print(value+1,file=db,end = ',')
        print(dia_a_predecir,file=db)

        for country in country_prediction_namelist:
    
            f = open('database_confirmed.csv')
            infected = []
            dia_inicio = 0
            for line in f:
                if(country == line.split(',')[1]):
                    country_data = []
                    data = line.replace('\n','').split(',')[4:]
                    for number in data:
                        if(number != '0'):
                            infected.append(int(number))
                        else:
                            dia_inicio += 1                    
            f.close()

            if(len(infected)<dias_a_usar):
                continue    
            print(country,end=',',file=db,sep=',')
            for value in infected[:dias_a_usar]:
                print(value,file=db,end = ',')
            if(len(infected)>=dia_a_predecir):
                print(infected[dia_a_predecir-1],file=db)
            else:
                print(-1,file=db)
        db.close()          


# In[16]:


        data_prediction = pd.read_csv("database_prediction.csv",sep=',') 


# In[17]:


        data_prediction


# In[18]:


        X_prediction = pd.DataFrame()
        for i in range(1,dias_a_usar+1):
            X_prediction[str(i)] = data_prediction[str(i)]
        Y_prediction = pd.DataFrame()
        Y_prediction[str(dia_a_predecir)] = data_prediction[str(dia_a_predecir)]
        print(X_prediction.shape, Y_prediction.shape)


# In[19]:

        predicciones.append(model.predict(X_prediction))
    predicciones_por_dia.append(predicciones)
    valores_por_dia.append(np.asarray(Y_prediction)[0][0])

for i,prediccion in enumerate(predicciones_por_dia):
    a = np.asarray(prediccion)
    print("dia:",i+N+1,"mean:",a.mean(),"mediana:",np.median(a),"min",a.min(),"max",a.max(),"std:",a.std(),"val:",valores_por_dia[i])
