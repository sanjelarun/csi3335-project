# Updates the Schools table
import pandas as pd;

def updateSchools(cursor):
    print("Adding new school data...")

    columns = ["schoolID", "name_full", "city", "state", "country"]
    data=pd.read_csv("Update_Assets/csvFiles/Schools.csv", na_values=['', ' '], encoding='ISO-8859-1', usecols=columns)
    data = data.where(pd.notnull(data), None)
    
    schoolsAdded = 0

    for row in data.iloc:

        newSchool = [
            row['schoolID'],
            row['name_full'],
            row['city'],
            row['state'],
            row['country']
        ]
        
        sql = '''INSERT IGNORE INTO schools (schoolID, school_name, school_city, school_state, school_country)
                VALUES(%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newSchool)
        schoolsAdded += exe
    
    print("Complete: {} new rows of school data added!".format(schoolsAdded))