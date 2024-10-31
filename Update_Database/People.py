# Updates the People table
import pandas as pd;

def updatePeople(cursor):
    print("Adding new people...")

    data=pd.read_csv("csvFiles/People.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    peopleAdded = 0

    for row in data.iloc:
        newPerson = [
            row['playerID'],
            row['birthYear'] if pd.notnull(row['birthYear']) else None,
            row['birthMonth'] if pd.notnull(row['birthMonth']) else None,
            row['birthDay'] if pd.notnull(row['birthDay']) else None,
            row['birthCountry'],
            row['birthState'],
            row['birthCity'],
            row['deathYear'] if pd.notnull(row['deathYear']) else None,
            row['deathMonth'] if pd.notnull(row['deathMonth']) else None,
            row['deathDay'] if pd.notnull(row['deathDay']) else None,
            row['deathCountry'],
            row['deathState'],
            row['deathCity'],
            row['nameFirst'],
            row['nameLast'],
            row['nameGiven'],
            row['weight'] if pd.notnull(row['weight']) else None,
            row['height'] if pd.notnull(row['height']) else None,
            row['bats'],
            row['throws'],
            row['debut'],
            row['finalGame'],
        ]
        
        sql = '''INSERT IGNORE INTO people (playerID,birthYear,birthMonth,birthDay,birthCountry,birthState,birthCity,deathYear,deathMonth,deathDay,deathCountry,deathState,deathCity,nameFirst,nameLast,nameGiven,weight,height,bats,throws,debutDate,finalGameDate)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        #execute html and extract needed info from result set
        exe = cursor.execute(sql,newPerson)
        peopleAdded += exe
    
    print("{} new People added!".format(peopleAdded))