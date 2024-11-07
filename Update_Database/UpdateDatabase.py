# Main Driver for our update database code

import pymysql
from UpdateScripts.People import updatePeople 
from UpdateScripts.Franchises import updateFranchises
from UpdateScripts.Batting import updateBatting
from UpdateScripts.Pitching import updatePitching
from UpdateScripts.Fielding import updateFielding
from UpdateScripts.FieldingOFSplit import updateFieldingOFSplit
from UpdateScripts.Appearances import updateAppearances
from UpdateScripts.PitchingPost import updatePitchingPost
from UpdateScripts.FieldingPost import updateFieldingPost
from UpdateScripts.BattingPost import updateBattingPost
from UpdateScripts.SeriesPost import updateSeriesPost
from UpdateScripts.AllStarFull import updateAllStarFull
from UpdateScripts.HallOfFame import updateHallOfFame
from UpdateScripts.Parks import updateParks
from UpdateScripts.Schools import updateSchools
from UpdateScripts.Managers import updateManagers
from UpdateScripts.ManagersHalf import updateManagersHalf
from UpdateScripts.Teams import updateTeams
from UpdateScripts.TeamsHalf import updateTeamsHalf
from UpdateScripts.AwardsPlayers import updateAwardsPlayers
from UpdateScripts.AwardsManagers import updateAwardsManagers
from UpdateScripts.AwardsSharePlayers import updateAwardsSharePlayers
from UpdateScripts.AwardsShareManagers import updateAwardsShareManagers
from UpdateScripts.Salaries import updateSalaries
from UpdateScripts.CollegePlaying import updateCollegePlaying

import csi3335f2024 as cfg

#connect to the db
con = pymysql.connect(host=cfg.mysql['location'],user=cfg.mysql['user'],password=cfg.mysql['password'],database=cfg.mysql['database'])


# retrieve info
try:
    cur = con.cursor()

    updatePeople(cur)
    updateBatting(cur)
    updatePitching(cur)

    updateFielding(cur)
    updateAppearances(cur)

    updateManagers(cur)
    updateManagersHalf(cur)

    updateFranchises(cur)
    updateTeams(cur)
    updateTeamsHalf(cur)

    updateFieldingOFSplit(cur)
   
    updatePitchingPost(cur)
    updateFieldingPost(cur)
    updateBattingPost(cur)
    updateSeriesPost(cur)

    updateAllStarFull(cur)
    updateAwardsPlayers(cur)
    updateAwardsManagers(cur)
    updateAwardsShareManagers(cur)
    updateAwardsSharePlayers(cur)
    updateHallOfFame(cur)
    
    updateParks(cur)
    
    updateSchools(cur)
    updateSalaries(cur)
    updateCollegePlaying(cur)

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

