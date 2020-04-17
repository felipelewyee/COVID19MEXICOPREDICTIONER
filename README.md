# COVID-19 Mexico Predictioner Red 3

Esta es una red secuencial simple para tratar de predecir el dato de número de contagiados de COVID19 en Mexico y que se da a las 19:00 horas por parte del gobierno.

La red aprende de los últimos N días de la curva, y usa información de superficie, población, latitud, longitud, dia de detección del primer caso, PIB, Gasto en Salud, Dia de inicio de la cuarentena, dia a predecir.

##Para ejecutar la prediccion

1. Ejecutar processing.sh, este script descarga el archivo time_series_covid19_confirmed_global.csv con datos de contagiados por pais. Este archivo se actualiza en internet aproximadamente a las 6:30pm con datos del día anterior, revisar que esté actualizado a la fecha del día de la predicción.

``` 
chmod +x processing.sh
```
```
./processing.sh
```

2. Abrir jupyter notebook (se requiere keras, tensorflow, pandas y numpy instaldos).

```
jupyter notebook COVID-19.ipynb
```

3. Actualizar dias_a_usar y dia_a_predecir. Como referencia, el 30 de marzo fue el día 33 de infeccion en Mexico, por lo que dia_a_predecir=33 y dias_a_usar=32.

4. Ejecutar todos los cuadros.

Creado por Juan Felipe Huan Lew Yee, Isaí Neftalí Rodríguez Rojas y Jorge Martín del Campo Ramírez.

## Fuente de datos

Superficie (km2), https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area

Población, https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population

Continente, https://simple.wikipedia.org/wiki/List_of_countries_by_continents

PIB (Millones de dolares), https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal) según estimados del 2019 del fondo monetario internacional, excepto por los siguientes paises:
-Datos del 2018 del banco mundial para Andorra,Cabo Verde,Cuba,Saint Vincent and the Grenadines,West Bank and Gaza,Guinea-Bissau
-Datos del 2017 de las naciones unidas para Monaco
-Uso datos de Google de 2015 para Liechtenstein
-Quite Holy See por PIB

Porcentaje de PIB invertido en salud, https://countryeconomy.com/government/expenditure/health
- Quite Liechtenstein, Taiwan, West Bank and Gaza y Kosovo por no encontrar dato

## Descripción de archivos


Analizador de propiedades, Carpeta que contiene los datos sin procesar como la población y el PIB de cada pais, en archivos tipo csv, así como los scrips:  analizador_de_propiedades.py que conjunta los datos anteriores y filter.py  para revisar los paises que se encuentren en  poblacion.csv

COVID-19.ipynb, Version en Jupyter Notebook de la red.

COVID-19.py,  Version de la red (la misma que en el Jupyter Notebook) dentro de un "for", para repetir la predicción muchas veces y obtener el promedio "mean" y  la desviacion estandar "std".

database.csv, Base de datos con el numero de casos históricos e informacion adicional como superficie, poblacion, PIB, etc... se crea automáticamente al ejecutar COVID-19.ipynb o COVID-19.py

database_confirmed.csv, Base de datos del Hospital John Hopkins con el numero de casos históricos procesada para tener informacion global de paises, se crea automáticamente al ejecutar processing.sh

database_prediction.csv, Base de datos con la informacion del pais a predecir, particularmente México, aunque se puede cambiar el país, se crea automáticamente al ejecutar COVID-19.ipynb o COVID-19.py

preprocessing.py, Script de pyhon para juntar la base de datos del hospital John Hopkins con los datos de propiedades_por_pais.csv, se ejecuta automáticamente al usar processing.sh

processing.sh, Descarga la base de datos del hospital John Hopkins y ejecuta varios scripts para su tratamiento.

propiedades_por_pais.csv, Base de datos con propiedades como superficie, poblacion, PIB, etc... fue creada con la informacion de la carpeta extractor_de_propiedades

time_series_covid19_confirmed_global.csv Base de datos del hospital John Hopkins, se descarga automáticamente al ejecutar processing.sh


