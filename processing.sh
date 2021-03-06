rm time_series_covid19_confirmed_global.csv
wget -O time_series_covid19_confirmed_global.csv https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv
sed -i -e 's/"//g' time_series_covid19_confirmed_global.csv
sed -i -e 's/Korea, South/Korea South/g' time_series_covid19_confirmed_global.csv
sed -i -e 's/Bonaire, Sint Eustatius and Saba/Bonaire Sint Eustatius and Saba/g' time_series_covid19_confirmed_global.csv
sed -i -e 's/Taiwan\*/Taiwan/g' time_series_covid19_confirmed_global.csv
python preprocessing.py > database_confirmed.csv

#Script de covid19_JHU_dashboard para actualizar manualmente la base de datos con la informacion mas reciente. Tomado de https://github.com/gohkokhan/covid19_JHU_dashboard
./get-data-from-JHU-dashboard.sh
python daily_updater.py > database_confirmed_new.csv
mv database_confirmed_new.csv database_confirmed.csv
rm *.json
