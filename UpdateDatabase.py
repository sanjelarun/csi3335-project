# Main Driver for our update database code

import pymysql
from Update_Assets.UpdateScripts.People import updatePeople 
from Update_Assets.UpdateScripts.Franchises import updateFranchises
from Update_Assets.UpdateScripts.Batting import updateBatting
from Update_Assets.UpdateScripts.Pitching import updatePitching
from Update_Assets.UpdateScripts.Fielding import updateFielding
from Update_Assets.UpdateScripts.FieldingOFSplit import updateFieldingOFSplit
from Update_Assets.UpdateScripts.Appearances import updateAppearances
from Update_Assets.UpdateScripts.PitchingPost import updatePitchingPost
from Update_Assets.UpdateScripts.FieldingPost import updateFieldingPost
from Update_Assets.UpdateScripts.BattingPost import updateBattingPost
from Update_Assets.UpdateScripts.Queries import createQueries
from Update_Assets.UpdateScripts.SeriesPost import updateSeriesPost
from Update_Assets.UpdateScripts.AllStarFull import updateAllStarFull
from Update_Assets.UpdateScripts.HallOfFame import updateHallOfFame
from Update_Assets.UpdateScripts.Parks import updateParks
from Update_Assets.UpdateScripts.Schools import updateSchools
from Update_Assets.UpdateScripts.Managers import updateManagers
from Update_Assets.UpdateScripts.ManagersHalf import updateManagersHalf
from Update_Assets.UpdateScripts.Teams import updateTeams
from Update_Assets.UpdateScripts.TeamsHalf import updateTeamsHalf
from Update_Assets.UpdateScripts.AwardsPlayers import updateAwardsPlayers
from Update_Assets.UpdateScripts.AwardsManagers import updateAwardsManagers
from Update_Assets.UpdateScripts.AwardsSharePlayers import updateAwardsSharePlayers
from Update_Assets.UpdateScripts.AwardsShareManagers import updateAwardsShareManagers
from Update_Assets.UpdateScripts.Salaries import updateSalaries
from Update_Assets.UpdateScripts.CollegePlaying import updateCollegePlaying
from Update_Assets.UpdateScripts.Seasons import createSeasons


import csi3335f2024 as cfg
from Update_Assets.UpdateScripts.Users import createUsers

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

    createSeasons(cur)

    createUsers(cur)
    createQueries(cur)

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

