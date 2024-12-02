# Updates the Batting table
import pandas as pd;

def updateSeriesPost(cursor):
    print("Adding new Series Post data...")

    data=pd.read_csv("Update_Assets/csvFiles/SeriesPost.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    seriesPostAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newSeries=[
            row["yearID"],
            row["round"],
            row["teamIDwinner"],
            row["teamIDloser"],
            row["wins"],
            row["losses"],
            row["ties"],
        ]
        
        sql = '''INSERT INTO seriespost (yearID,round,teamIDwinner,teamIDloser,wins,losses,ties)
                VALUES(%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newSeries)
        seriesPostAdded += exe
    
    print("Complete: {} new rows of series post data!".format(seriesPostAdded))