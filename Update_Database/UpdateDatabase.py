# Main Driver for our update database code

import pymysql
from People import updatePeople 

import csi3335f2024 as cfg

#connect to the db
con = pymysql.connect(host=cfg.mysql['location'],user=cfg.mysql['user'],password=cfg.mysql['password'],database=cfg.mysql['database'])


# retrieve info
try:

   
    cur = con.cursor()

    updatePeople(cur)

    # sql = '''SELECT yearID, ballots, votes, inducted, birthYear, deathYear 
    #         FROM halloffame NATURAL JOIN people 
    #         WHERE nameFirst=%s AND nameLast=%s;'''
    # #execute html and extract needed info from result set
    # cur.execute(sql,[firstName,lastName])
    # results = cur.fetchall()
   

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

