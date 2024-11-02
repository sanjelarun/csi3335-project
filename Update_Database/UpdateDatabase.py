# Main Driver for our update database code

import pymysql
from People import updatePeople 
from Batting import updateBatting
from FieldingOFSplit import updateFieldingOFSplit
from AllStarFull import updateAllStarFull
from SeriesPost import updateSeriesPost
from AwardsManagers import updateAwardsManagers
from HallOfFame import updateHallOfFame
from Parks import updateParks
from Managers import updateManagers
from FieldingPost import updateFieldingPost
from TeamsHalf import updateTeamsHalf
from AwardsSharePlayers import updateAwardsSharePlayers
from Schools import updateSchools

import csi3335f2024 as cfg

#connect to the db
con = pymysql.connect(host=cfg.mysql['location'],user=cfg.mysql['user'],password=cfg.mysql['password'],database=cfg.mysql['database'])


# retrieve info
try:
    cur = con.cursor()

    updatePeople(cur)
    updateBatting(cur)
    updateFieldingOFSplit(cur)
    updateAllStarFull(cur) 
    updateSeriesPost(cur)
    updateAwardsManagers(cur)
    updateHallOfFame(cur)
    updateParks(cur)
    updateManagers(cur)
    updateFieldingPost(cur)
    updateTeamsHalf(cur)
    updateAwardsSharePlayers(cur)
    updateSchools(cur)


except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

