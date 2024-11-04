# Main Driver for our update database code

import pymysql
from People import updatePeople 
from Batting import updateBatting
from Franchises import updateFranchises
from Fielding import updateFielding
from FieldingOFSplit import updateFieldingOFSplit
from Appearances import updateAppearances
from PitchingPost import updatePitchingPost
from SeriesPost import updateSeriesPost
from AllStarFull import updateAllStarFull
from HallOfFame import updateHallOfFame
from ManagersHalf import updateManagersHalf
from AwardsManagers import updateAwardsManagers
from AwardsShareManagers import updateAwardsShareManagers
from Salaries import updateSalaries


import csi3335f2024 as cfg

#connect to the db
con = pymysql.connect(host=cfg.mysql['location'],user=cfg.mysql['user'],password=cfg.mysql['password'],database=cfg.mysql['database'])


# retrieve info
try:
    cur = con.cursor()

    updatePeople(cur)
    updateBatting(cur)
    updateFranchises(cur)
    updateFielding(cur)
    updateAppearances(cur)
    # Update managers first
    updateManagersHalf(cur)
    updateFieldingOFSplit(cur)
    updateAllStarFull(cur) 
    updatePitchingPost(cur)
    updateSeriesPost(cur)
    updateAwardsManagers(cur)
    updateAwardsShareManagers(cur)
    updateHallOfFame(cur)
    updateSalaries(cur)

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

