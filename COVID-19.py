#!/usr/bin/env python
# coding: utf-8

# # Red para COVID-19

# Creado por Juan Felipe Huan Lew Yee, Neftalí Isaí Rodríguez Rojas y Jorge Martín del Campo Ramírez.

import numpy as np
import keras
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense,Dropout

predicciones_por_dia = []
valores_por_dia = []
dia_a_predecir = int(input("Dia a predecir (Ref. 04/04/2020 es el dia 38)? "))
dias_a_usar = int(input("Cuantos dias previos quiere usar? "))
dias_a_futuro = int(input("Cuantos dias a futuro es la predicción? "))
repeticiones = int(input("Cuantas repeticiones quiere? "))
predicciones = []
for i in range(repeticiones):

# In[1]:

# Definimos la lista de paises que analizaremos. (Hay más paises en la base de datos de John Hopkins)

# In[2]:

    country_namelist = ['Albania', 'Algeria', 'Argentina', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Congo (Brazzaville)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Eritrea', 'Fiji', 'Finland', 'France', 'Germany', 'Ghana', 'Greece', 'Honduras', 'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kuwait', 'Lebanon', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Montenegro', 'Morocco', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'San Marino', 'Saudi Arabia', 'Serbia', 'Singapore', 'South Africa', 'Spain', 'Thailand', 'Tunisia', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'US', 'Venezuela', 'Zimbabwe', 'Libya', 'Botswana']
    #['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Andorra', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea South', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Maldives', 'Malta', 'Mauritania', 'Mauritius', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tanzania', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'US', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zambia', 'Zimbabwe', 'Dominica', 'Grenada', 'Mozambique', 'Syria', 'Timor-Leste', 'Belize', 'Laos', 'Libya', 'Guinea-Bissau', 'Mali', 'Saint Kitts and Nevis', 'Burma', 'Botswana', 'Burundi', 'Sierra Leone', 'Malawi']


# Abrimos la base de datos de Superficie, Población y Continente por país, creamos un objeto para cada país. Posterirmente, abirmos la base de datos de John Hopkins y extraemos los datos de infectos por día y la latitud y longitud de cada país. También calculamos el día de inicio de la infección

# In[3]:

    db = open('database.csv','w')

    print("Pais","Area","poblacion","Namerica","Samerica","Europe","Asia","Oceania","Africa","lat","longitud","Dia_inicio","PIB","Gasto_Salud","Cuarentena","Dia",end=',',file=db,sep=',')
    for value in range(dias_a_usar):
        print(value+1,file=db,end = ',')
    print("dia_a_predecir",file=db)

    for country in country_namelist:
        f = open('propiedades_por_pais.csv')
        for line in f:
            if(country == line.replace('\n','').split(',')[0]):
                pais=line.replace('\n','').split(',')[0]
                superficie=line.replace('\n','').split(',')[1]
                poblacion=line.replace('\n','').split(',')[2]
                namerica=line.replace('\n','').split(',')[3]
                samerica=line.replace('\n','').split(',')[4]
                europe=line.replace('\n','').split(',')[5]
                asia=line.replace('\n','').split(',')[6]
                oceania=line.replace('\n','').split(',')[7]
                africa=line.replace('\n','').split(',')[8]
                pib=line.replace('\n','').split(',')[9]
                salud_pib=line.replace('\n','').split(',')[10]            
                cuarentena=line.replace('\n','').split(',')[11]            
        f.close()
    
        f = open('database_confirmed.csv')
        infected = []
        dia_inicio = 0
        for line in f:
            if(country == line.split(',')[1]):
                lat = float(line.split(',')[2])
                longitud = float(line.split(',')[3])
                country_data = []
                data = line.replace('\n','').split(',')[4:]
                for number in data:
                    if(number != '0'):
                        infected.append(int(number))
                    else:
                        dia_inicio += 1                    
        f.close()

        if(len(infected)<=dias_a_usar+dias_a_futuro):
#            print(pais,superficie,poblacion,namerica,samerica,europe,asia,oceania,africa,lat,long,pib,salud_pib,len(infected))
            continue
        for i in range(0,len(infected)-dias_a_usar-dias_a_futuro):
            print(pais,superficie,poblacion,namerica,samerica,europe,asia,oceania,africa,lat,longitud,dia_inicio,pib,salud_pib,cuarentena,i+dias_a_usar+1,end=',',file=db,sep=',')
            for j in range(dias_a_usar):
                print(infected[i+j],file=db,end = ',')
            print(infected[i+dias_a_usar+dias_a_futuro-1],file=db)
    db.close()   

# Leamos la base de datos que acabamos de crear.

# In[5]:


    data = pd.read_csv("database.csv",sep=',') 


# Imprimimos la base de datos

# In[6]:


    data


# Normalizamos algunas variables

# In[7]:


    print("Area")
    area = data.Area #returns a numpy array
    areamax=area.max()
    areamin=area.min()
    normalized_area=(area-area.min())/(area.max()-area.min())
    print(areamin,areamax)
    data['Area'] = normalized_area
    print(areamin,areamax)

    print("Poblacion")
    poblacion = data.poblacion #returns a numpy array
    poblacionmax=poblacion.max()
    poblacionmin=poblacion.min()
    normalized_poblacion=(poblacion-poblacion.min())/(poblacion.max()-poblacion.min())
    print(poblacionmin,poblacionmax)
    data['poblacion'] = normalized_poblacion
    print(poblacionmin,poblacionmax)

    print("lat")
    lat = data.lat #returns a numpy array
    latmax=lat.max()
    latmin=lat.min()
    normalized_lat=(lat-lat.min())/(lat.max()-lat.min())
    print(latmin,latmax)
    data['lat'] = normalized_lat
    print(latmin,latmax)

    print("longitud")
    longitud = data.longitud #returns a numpy array
    longitudmax=longitud.max()
    longitudmin=longitud.min()
    normalized_longitud=(longitud-longitud.min())/(longitud.max()-longitud.min())
    print(longitudmin,longitudmax)
    data['longitud'] = normalized_longitud
    print(longitudmin,longitudmax)

    print("Dia_inicio")
    Dia_inicio = data.Dia_inicio #returns a numpy array
    Dia_iniciomax=Dia_inicio.max()
    Dia_iniciomin=Dia_inicio.min()
    normalized_Dia_inicio=(Dia_inicio-Dia_inicio.min())/(Dia_inicio.max()-Dia_inicio.min())
    print(Dia_iniciomin,Dia_iniciomax)
    data['Dia_inicio'] = normalized_Dia_inicio
    print(Dia_iniciomin,Dia_iniciomax)

    print("PIB")
    PIB = data.PIB #returns a numpy array
    PIBmax=PIB.max()
    PIBmin=PIB.min()
    normalized_PIB=(PIB-PIB.min())/(PIB.max()-PIB.min())
    print(PIBmin,PIBmax)
    data['PIB'] = normalized_PIB
    print(PIBmin,PIBmax)

    print("Gasto_Salud")
    Gasto_Salud = data.Gasto_Salud #returns a numpy array
    Gasto_Saludmax=Gasto_Salud.max()
    Gasto_Saludmin=Gasto_Salud.min()
    normalized_Gasto_Salud=(Gasto_Salud-Gasto_Salud.min())/(Gasto_Salud.max()-Gasto_Salud.min())
    print(Gasto_Saludmin,Gasto_Saludmax)
    data['Gasto_Salud'] = normalized_Gasto_Salud
    print(Gasto_Saludmin,Gasto_Saludmax)

    print("Cuarentena")
    Cuarentena = data.Cuarentena #returns a numpy array
    Cuarentenamax=Cuarentena.max()
    Cuarentenamin=Cuarentena.min()
    normalized_Cuarentena=(Cuarentena-Cuarentena.min())/(Cuarentena.max()-Cuarentena.min())
    print(Cuarentenamin,Cuarentenamax)
    data['Cuarentena'] = normalized_Cuarentena
    print(Cuarentenamin,Cuarentenamax)

    print("Dia")
    Dia = data.Dia #returns a numpy array
    Diamax=Dia.max()
    Diamin=Dia.min()
    normalized_Dia=(Dia-Dia.min())/(Dia.max()-Dia.min())
    print(Diamin,Diamax)
    data['Dia'] = normalized_Dia
    print(Diamin,Diamax)

    infectedmin = 1
    infectedmax = 1
    for i in range(dias_a_usar):
        infected = data[str(i+1)]
        infectedmax = max(infectedmax,np.amax(infected))

    for i in range(dias_a_usar):
        infected = data[str(i+1)]
        normalize_infected = (infected-infectedmin)/(infectedmax-infectedmin)
        data[str(i+1)] = normalize_infected

# Imprimimos la base de datos normalizada

# In[8]:


    data


# Creamos un conjunto X y un conjunto Y y dividimos train y test

# In[9]:


    from sklearn.model_selection import train_test_split
    X = pd.DataFrame()
    X['Area'] = data['Area']
    X['poblacion'] = data['poblacion']
#    X['Namerica'] = data['Namerica']
#    X['Samerica'] = data['Samerica']
#    X['Europe'] = data['Europe']
#    X['Asia'] = data['Asia']
#    X['Oceania'] = data['Oceania']
#    X['Africa'] = data['Africa']
    X['lat'] = data['lat']
    X['longitud'] = data['longitud']
    X['Dia_inicio'] = data['Dia_inicio']
    X['PIB'] = data['PIB']
    X['Gasto_Salud'] = data['Gasto_Salud']
    X['Cuarentena'] = data['Cuarentena']
    X['Dia'] = data['Dia']
    for i in range(1,dias_a_usar+1):
        X[str(i)] = data[str(i)]
    Y = pd.DataFrame()
    Y["dia_a_predecir"] = data["dia_a_predecir"]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)


# Creamos la red neuronal

# In[10]:


    model = Sequential()
    model.add(Dense(32, input_dim=dias_a_usar+9, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))


# Compilamos la red

# In[11]:


    model.compile(loss='MAPE', optimizer='adam')


# Entrenamos la red

# In[12]:


    history = model.fit(X_train, y_train, epochs=500, validation_data=(X_test,y_test),verbose=2)


# In[13]:


#        import matplotlib.pyplot as plt

# Plot training & validation loss values
#        plt.plot(history.history['loss'])
#        plt.plot(history.history['val_loss'])
#        plt.title('Model loss')
#        plt.ylabel('Loss')
#        plt.xlabel('Epoch')
#        plt.legend(['Train', 'Test'], loc='upper left')
#        plt.show()


# Realizamos predicciones del test

# In[14]:


    model.predict(X_test)


# Comprobamos

# In[15]:


    y_test


# # Predicción

# In[16]:


    country_prediction_namelist = ['Mexico']


# In[17]:

    db = open('database_prediction.csv','w')

    print("Pais","Area","poblacion","Namerica","Samerica","Europe","Asia","Oceania","Africa","lat","longitud","Dia_inicio","PIB","Gasto_Salud","Cuarentena","Dia",end=',',file=db,sep=',')
    for value in range(dias_a_usar):
        print(value+1,file=db,end = ',')
    print("dia_a_predecir",file=db)

    for country in country_prediction_namelist:
        f = open('propiedades_por_pais.csv')
        for line in f:
            if(country == line.replace('\n','').split(',')[0]):
                pais=line.replace('\n','').split(',')[0]
                superficie=line.replace('\n','').split(',')[1]
                poblacion=line.replace('\n','').split(',')[2]
                namerica=line.replace('\n','').split(',')[3]
                samerica=line.replace('\n','').split(',')[4]
                europe=line.replace('\n','').split(',')[5]
                asia=line.replace('\n','').split(',')[6]
                oceania=line.replace('\n','').split(',')[7]
                africa=line.replace('\n','').split(',')[8]
                pib=line.replace('\n','').split(',')[9]
                salud_pib=line.replace('\n','').split(',')[10]            
                cuarentena=line.replace('\n','').split(',')[11]            
        f.close()
    
        f = open('database_confirmed.csv')
        infected = []
        dia_inicio = 0
        for line in f:
            if(country == line.split(',')[1]):
                lat = float(line.split(',')[2])
                longitud = float(line.split(',')[3])
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
        print(pais,superficie,poblacion,namerica,samerica,europe,asia,oceania,africa,lat,longitud,dia_inicio,pib,salud_pib,cuarentena,dia_a_predecir,end=',',file=db,sep=',')
        for value in infected[dia_a_predecir-dias_a_usar-dias_a_futuro:dia_a_predecir-dias_a_futuro]:
            print(value,file=db,end = ',')
        if(len(infected)>=dia_a_predecir):
            print(infected[dia_a_predecir-1],file=db)
        else:
            print(-1,file=db)

    db.close()          


# In[18]:


    data_prediction = pd.read_csv("database_prediction.csv",sep=',') 


# In[19]:


    data_prediction


# In[20]:


    area_prediction = data_prediction.Area #returns a numpy array
    normalized_area_prediction=(area_prediction-areamin)/(areamax-areamin)
    data_prediction['Area'] = normalized_area_prediction

    poblacion_prediction = data_prediction.poblacion #returns a numpy array
    normalized_poblacion_prediction=(poblacion_prediction-poblacionmin)/(poblacionmax-poblacionmin)
    data_prediction['poblacion'] = normalized_poblacion_prediction

    lat_prediction = data_prediction.lat #returns a numpy array
    normalized_lat_prediction=(lat_prediction-latmin)/(latmax-latmin)
    data_prediction['lat'] = normalized_lat_prediction

    longitud_prediction = data_prediction.longitud #returns a numpy array
    normalized_longitud_prediction=(longitud_prediction-longitudmin)/(longitudmax-longitudmin)
    data_prediction['longitud'] = normalized_longitud_prediction

    Dia_inicio_prediction = data_prediction.Dia_inicio #returns a numpy array
    normalized_Dia_inicio_prediction=(Dia_inicio_prediction-Dia_iniciomin)/(Dia_iniciomax-Dia_iniciomin)
    data_prediction['Dia_inicio'] = normalized_Dia_inicio_prediction
        
    PIB_prediction = data_prediction.PIB #returns a numpy array
    normalized_PIB_prediction=(PIB_prediction-PIBmin)/(PIBmax-PIBmin)
    data_prediction['PIB'] = normalized_PIB_prediction
        
    Gasto_Salud_prediction = data_prediction.Gasto_Salud #returns a numpy array
    normalized_Gasto_Salud_prediction=(Gasto_Salud_prediction-Gasto_Saludmin)/(Gasto_Saludmax-Gasto_Saludmin)
    data_prediction['Gasto_Salud'] = normalized_Gasto_Salud_prediction
        
    Cuarentena_prediction = data_prediction.Cuarentena #returns a numpy array
    normalized_Cuarentena_prediction=(Cuarentena_prediction-Cuarentenamin)/(Cuarentenamax-Cuarentenamin)
    data_prediction['Cuarentena'] = normalized_Cuarentena_prediction
        
    Dia_prediction = data_prediction.Dia #returns a numpy array
    normalized_Dia_prediction=(Dia_prediction-Diamin)/(Diamax-Diamin)
    data_prediction['Dia'] = normalized_Dia_prediction
        
    for i in range(dias_a_usar):
        infected = data_prediction[str(i+1)]
        normalize_infected = (infected-infectedmin)/(infectedmax-infectedmin)
        data_prediction[str(i+1)] = normalize_infected

# In[21]:


    data_prediction


# In[22]:


    from sklearn.model_selection import train_test_split
    X_prediction = pd.DataFrame()
    X_prediction['Area'] = data_prediction['Area']
    X_prediction['poblacion'] = data_prediction['poblacion']
#    X_prediction['Namerica'] = data_prediction['Namerica']
#    X_prediction['Samerica'] = data_prediction['Samerica']
#    X_prediction['Europe'] = data_prediction['Europe']
#    X_prediction['Asia'] = data_prediction['Asia']
#    X_prediction['Oceania'] = data_prediction['Oceania']
#    X_prediction['Africa'] = data_prediction['Africa']
    X_prediction['lat'] = data_prediction['lat']
    X_prediction['longitud'] = data_prediction['longitud']
    X_prediction['Dia_inicio'] = data_prediction['Dia_inicio']
    X_prediction['PIB'] = data_prediction['PIB']
    X_prediction['Gasto_Salud'] = data_prediction['Gasto_Salud']
    X_prediction['Cuarentena'] = data_prediction['Cuarentena']
    X_prediction['Dia'] = data_prediction['Dia']
    for i in range(1,dias_a_usar+1):
        X_prediction[str(i)] = data_prediction[str(i)]
    Y_prediction = pd.DataFrame()
    Y_prediction["dia_a_predecir"] = data_prediction["dia_a_predecir"]
    print(X_prediction.shape, Y_prediction.shape) 


# In[23]:


    predicciones.append(model.predict(X_prediction))
predicciones_por_dia.append(predicciones)
valores_por_dia.append(np.asarray(Y_prediction)[0][0])

for i,prediccion in enumerate(predicciones_por_dia):
    a = np.asarray(prediccion)
    print("dia:",dia_a_predecir,"mean:",a.mean(),"mediana:",np.median(a),"min",a.min(),"max",a.max(),"std:",a.std(),"val:",valores_por_dia[i])
