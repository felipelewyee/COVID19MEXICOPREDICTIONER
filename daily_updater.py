#Countries to update in the databse (selected by the user)
countries = 'Brazil','Georgia','Greece','North Macedonia','Norway','Pakistan','Romania','Mexico'

#Open the database
f1 = open('database_confirmed.csv')

#Loop over countries
for line1 in f1:
    country = line1.split(',')[1]

    #Check if the country is in the list to updates
    if(country in countries):
    
        #Open the database
        f2 = open('JHU_new3.json')

        #Look for the country and take the number of confirmed cases
        for line2 in f2:
            if(country in line2):
                confirmed = line2.replace('\"attributes\":','').replace('{','').replace('}','').replace('\'','').split(',')[6].split(':')[1]
                break
        f2.close()

        #Check if the number is not already listed in the database and add it
        if confirmed not in line1 and int(confirmed) >= int(line1.split(',')[-1]):
            print(line1.replace('\n','')+','+confirmed)
        else:
            print(line1.replace('\n',''))
    else:    
        print(line1.replace('\n',''))
