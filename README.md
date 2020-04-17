Esta es una red secuencial simple para tratar de predecir el dato de número de contagiados de COVID19 en Mexico y que se da a las 19:00 horas por parte del gobierno. Las predicciones de la red se actualizan en la página https://elquimicoartificial.wordpress.com/

Creado por Juan Felipe Huan Lew Yee, Isaí Neftalí Rodríguez Rojas y Jorge Martín del Campo Ramírez.

**Para ejecutar la prediccion:**

**1)** Ejecutar processing.sh, este script descarga el archivo time_series_covid19_confirmed_global.csv con datos de contagiados por pais. Este archivo se actualiza en internet aproximadamente a las 5:30pm con datos del día anterior, revisar que esté actualizado a la fecha del día de la predicción.

chmod +x processing.sh

./processing.sh

-----------------------------------Jupyter Notebook-----------------------------------
**2)** Abrir jupyter notebook o ejecutar con python (se requiere keras, tensorflow, pandas y numpy instaldos).

jupyter notebook COVID-19.ipynb

**3)** Actualizar dias_a_usar y dia_a_predecir. Como referencia, el 30 de marzo fue el día 33 de infeccion en Mexico, por lo que dia_a_predecir=33 y dias_a_usar=32.

**4)** Ejecutar todos los cuadros.

-----------------------------------Python-----------------------------------
**2)** Ejecutar script con python (se requiere keras, tensorflow, pandas y numpy instaldos).

python COVID-19.py

**3)** Ingresar el número del día a predecir. Como referencia, el 30 de marzo fue el día 33 de infeccion en Mexico, por lo que dia_a_predecir=33 y dias_a_usar=32.

**4)** Ingresar el número de días de diferencia entre el último día a usar y día a predecir. Ejemplo, para predecir el día 50 con los primeros 49 días este dato valdrá 1, para predecir el día 50 con los primeros 48 días este dato valdrá 2.

**5)** Ingresar el número de repeticiones de la predicción. La red se entrenará este número de veces desde diferentes pesos de partida y se obtendrá un promedio de las predicciones. Este es el dato que se usa para actualizar la tabla de https://elquimicoartificial.wordpress.com

**********************************Descripción de archivos*******************************

COVID-19.ipynb, Version en Jupyter Notebook de la red.

COVID-19.py,  Version de la red (la misma que en el Jupyter Notebook) dentro de un "for", para repetir la predicción muchas veces y obtener el promedio "mean" y  la desviacion estandar "std".

database.csv, Base de datos con el numero de casos históricos e informacion adicional como superficie, poblacion, PIB, etc... se crea automáticamente al ejecutar COVID-19.ipynb o COVID-19.py

database_confirmed.csv, Base de datos del Hospital John Hopkins con el numero de casos históricos procesada para tener informacion global de paises, se crea automáticamente al ejecutar processing.sh

database_prediction.csv, Base de datos con la informacion del pais a predecir, particularmente México, aunque se puede cambiar el país, se crea automáticamente al ejecutar COVID-19.ipynb o COVID-19.py

preprocessing.py, Script de pyhon para juntar la base de datos del hospital John Hopkins con los datos de propiedades_por_pais.csv, se ejecuta automáticamente al usar processing.sh

processing.sh, Descarga la base de datos del hospital John Hopkins y ejecuta varios scripts para su tratamiento.

tester.py Script para realizar predicciones de todos los días de la curva de México y evaluar la calidad de la red.
