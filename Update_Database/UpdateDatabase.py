# Main Driver for our update database code

import pymysql
from People import updatePeople 
from Batting import updateBatting
from Franchises import updateFranchises
from Fielding import updateFielding
from FieldingOFSplit import updateFieldingOFSplit
from Appearances import updateAppearances
from PitchingPost import updatePitchingPost
from FieldingPost import updateFieldingPost
from SeriesPost import updateSeriesPost
from AllStarFull import updateAllStarFull
from HallOfFame import updateHallOfFame
from Parks import updateParks
from Schools import updateSchools
from Managers import updateManagers
from ManagersHalf import updateManagersHalf
from TeamsHalf import updateTeamsHalf
from AwardsManagers import updateAwardsManagers
from AwardsSharePlayers import updateAwardsSharePlayers
from AwardsShareManagers import updateAwardsShareManagers
from Salaries import updateSalaries
from AwardsPlayers import update_awards_players
from CollegePlaying import update_college_playing
from Pitching import update_pitching
from Teams import update_teams
from BattingPost import update_batting_post

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

    updateManagers(cur)
    updateManagersHalf(cur)

    updateTeamsHalf(cur)

    updateFieldingOFSplit(cur)
    updateAllStarFull(cur)
    updatePitchingPost(cur)
    updateFieldingPost(cur)
    updateSeriesPost(cur)

    updateAwardsManagers(cur)
    updateAwardsShareManagers(cur)
    updateAwardsSharePlayers(cur)
    updateHallOfFame(cur)
    
    updateParks(cur)
    
    updateSchools(cur)
    updateSalaries(cur)

    # Mitchell's table updates
    update_awards_players(cur)
    update_college_playing(cur)
    update_pitching(cur)
    update_teams(cur)
    update_batting_post(cur)

except Exception:
    con.rollback()
    print("Database exception")
    raise
else: 
    con.commit()
finally:
    con.close()

