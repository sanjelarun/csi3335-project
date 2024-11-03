# Main Driver for our update database code

import pymysql
from People import updatePeople 
from Batting import updateBatting
from Franchises import updateFranchises
from Fielding import updateFielding
from Appearances import updateAppearances
from PitchingPost import updatePitchingPost
from ManagersHalf import updateManagersHalf
from AwardsShareManagers import updateAwardsShareManagers

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
    updatePitchingPost(cur)
    # Update managers first
    updateManagersHalf(cur)
    updateAwardsShareManagers(cur)

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

