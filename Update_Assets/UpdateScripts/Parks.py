# Updates the Parks table
import pandas as pd;

def updateParks(cursor):
    print("Adding new parks data...")

    data=pd.read_csv("Update_Assets/csvFiles/Parks.csv", na_values=['', ' '], encoding='ISO-8859-1')
    data = data.where(pd.notnull(data), None)
    
    parksAdded = 0

    for row in data.iloc:

        newPark = [
            row['parkkey'],
            row['parkname'],
            row['parkalias'],
            row['city'],
            row["state"],
            row["country"],
        ]
        
        sql = '''INSERT IGNORE INTO parks (parkID, park_name, park_alias, city, state, country)
                VALUES(%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newPark)
        parksAdded += exe
    
    print("Complete: {} new rows of park data added!".format(parksAdded))