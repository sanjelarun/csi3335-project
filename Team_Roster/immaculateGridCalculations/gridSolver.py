from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Batting, Team, Pitching, AllStarFull, Awards, Appearances, Season
from sqlalchemy import func, and_, literal_column
from immaculateGridCalculations.complexFormulas import get_war, get_grouped_fielding



# Retrieves a list of all team names from the database.
# Returns: A list of team names as strings.
def getAllTeams():
    teams = db.session.query(Team.team_name).all() 
    team_list = [team.team_name for team in teams]
    return team_list

# Retrieves all players associated with a given team.
# Notes: The query ensures that players are grouped by their playerID and the team's name.
def getPlayersByTeam(team_name):
    return (
        db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID"),
            literal_column('TRUE').label('isTeamCheck') 
            )
        .select_from(Team)
        .join(Batting, (Batting.teamID == Team.teamID) & (Batting.yearID == Team.yearID))
        .filter(Team.team_name == team_name)
        .group_by(Batting.playerID)
    )


# Retrieves all players who have achieved a minimum number of wins in a season.
# Parameters:
# - numWins (int): The minimum number of wins required.
# Notes: 
# - Only pitchers are awarded "wins," as this statistic is specific to the Pitching table.
# - The query joins People, Pitching, and Team tables to ensure accurate filtering and grouping.
def getPlayerWinsBySeason(numWins):
    return (
        db.session.query(
            Pitching.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
        .join(Team, (Team.yearID == Pitching.yearID) & (Team.teamID == Pitching.teamID))
        .group_by(Pitching.playerID,Pitching.yearID,Pitching.teamID)
        .having(func.sum(Pitching.p_W)>=numWins)
    )

# Retrieves all players who have achieved a minimum of .300 AVG in a season.
# Notes: 
def getPlayerAvgBySeason():
    return (
        db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
        )
        .join(Team, (Team.yearID == Batting.yearID) & (Team.teamID == Batting.teamID))
        .group_by(Batting.playerID, Batting.yearID, Batting.teamID)
        .having((func.sum(Batting.b_H)/func.sum(Batting.b_AB)) >= .300)
        )

# Fetches the career average of players with a minimum of .300 AVG
def getPlayerAvgByCareer():
    return(
        db.session.query(
            Batting.playerID.label("playerID")
        )
        .group_by(Batting.playerID)
        .having((func.sum(Batting.b_H)/func.sum(Batting.b_AB))>=.300)
    )


# Retrieves all players who have achieved a minimum SV in a season.
# Parameters:
# - svNum (int): The minimum SV required.
def getPlayerSVBySeason(svNum):
    return (
        db.session.query(
            Pitching.playerID.label("playerID"),
            Pitching.teamID.label("teamID")
        )
        .join(Team, (Team.teamID == Pitching.teamID) & (Team.yearID == Pitching.yearID))
        .group_by(Pitching.playerID, Pitching.teamID, Pitching.yearID)
        .having(func.sum(Pitching.p_SV) >= svNum)
    )

# All players with a CAREER K over a certain amount
# Parameters:
# - kNum (int): The min K
# Notes: 
# - K is also known as SO, strike outs 
def getPlayerKByCareer(kNum):
    return (
        db.session.query(
            Batting.playerID.label("playerID"),
        )
        .group_by(Batting.playerID)
        .having(func.sum(Batting.b_SO) >= kNum)
    )


# Fetches the players with 30+ stolen bases in a season
# Parameters:
#   - maxSB (int): maximum stolen bases
def getPlayerSeasonSB(maxSB):
    return(
        db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
        )
        .join(Team, (Team.yearID == Batting.yearID) & (Team.teamID == Batting.teamID))
        .group_by(Batting.playerID, Batting.yearID, Batting.teamID)
        .having(func.sum(Batting.b_SB) >= maxSB)
    )

# Fetches the pitchers with career wins above a given number
# Parameters:
#   - winNum (int): The minimum career wins
def getPlayerCareerWins(winNum):
    return (
        db.session.query(
            Pitching.playerID.label("playerID")
        )
        .group_by(Pitching.playerID)
        .having(func.sum(Pitching.p_W)>=winNum)
    )

#Gets the war of every player, used by the war questions
def getPlayerWars():
    grouped_fielding= get_grouped_fielding()
    war = get_war(grouped_fielding)
    return(
        db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID"),
            war.label("WAR"),
            Season.s_wBB,
            Season.s_wHBP,
            Season.s_w1B,
            Season.s_w2B,
            Season.s_w3B,
            Season.s_wHR,
            Season.s_wOBA,
            Season.s_wOBAScale,
            Season.s_runSB,
            Season.s_runCS,
            Season.s_SB,
            Season.s_CS,
            Season.s_1B,
            Season.s_BB,
            Season.s_HBP,
            Season.s_IBB,
            Season.s_G,
            Season.s_R_W,
            Season.s_PA,
        )
        .join(grouped_fielding,and_(
            Batting.playerID == grouped_fielding.c.playerID,
            Batting.yearID == grouped_fielding.c.yearID,
            Batting.teamID == grouped_fielding.c.teamID,
            Batting.stint == grouped_fielding.c.stint
        ))
        .join(Season,Batting.yearID == Season.yearID)
        .group_by(Batting.playerID,Batting.yearID, Batting.teamID)
        .subquery()
    )

# Fetches the players with a WAR value greater than a given number
# Parameters:
#   - minWAR : minimum WAR value
def getPlayerWARSeason(minWAR):
    wars = getPlayerWars()
    return(
        db.session.query(
            wars.c.playerID.label("playerID"),
            wars.c.teamID.label("teamID"),
        )
        .filter( wars.c.WAR >=minWAR)
    )

# Fetches the players above a certain WAR value for their career
# Parameters:
#   - minWAR : minimum WAR value
def getPlayerWARCareer(minWAR):
    wars = getPlayerWars()
    return(
        db.session.query(
            wars.c.playerID.label("playerID"),
            wars.c.teamID.label("teamID"),
        )
        .group_by(wars.c.playerID)
        .having( func.sum(wars.c.WAR) >=minWAR)
    )

# Fetches players that have been designated hitters
def getPlayerDesignatedHitter():
    return(
        db.session.query(
            Appearances.playerID.label("playerID"),
            Appearances.teamID.label("TeamID")
        )
        .group_by(Appearances.playerID, Appearances.teamID)
        .having(func.sum(Appearances.G_dh) > 0)
    )

# Fetches the teams that have won the world series
def getWorldSeriesChamp():
    return(
        db.session.query(
            Team.teamID.label("teamID"),
        )
        .group_by(Team.teamID, Team.yearID)
        .filter(Team.WSWin == 'Y')
    )

# All players with a CAREER era over a certian amount
# Parameters:
# - maxERA (int): The maximum career ERA required
# Notes: 
# - Career ERA cannot be caluclated using stint ERA, so I had to do the full calculaton
def getPlayerCareerEra(maxERA):
    return (
        db.session.query(Pitching.playerID.label("playerID"))
        .group_by(Pitching.playerID)
        .having(#Career ERA = Career ER / (Career IPOuts/3) * 9
            (
                func.sum(Pitching.p_ER)
                /
                (func.sum(Pitching.p_IPOuts)/3)
                *9
            ) <= maxERA
        )
    )

# All players with a SEASON RBI over a certian amount, while on a certian team
# Parameters:
# - minRBI (int): The minimum season RBI required
# Notes: 
def getPlayerSeasonRBI(minRBI):
    query = (db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
            .group_by(Batting.playerID, Batting.yearID)
            .having(func.sum(Batting.b_RBI) >= minRBI))

    return query

# All players with a SEASON Strikeout over a certian amount, while on a certian team
# Parameters:
# - minK (int): The minimum season Strikeouts required
# - teamName: the name of the team they achieved this stat on
# Notes: 
def getPlayerSeasonK(minK):
    query = (
        db.session.query(
            Pitching.playerID,
            Pitching.teamID.label("teamID")
        )
        .group_by(Pitching.playerID, Pitching.yearID, Pitching.teamID)  # Group by playerID, yearId, and teamID
        .having(func.sum(Pitching.p_SO) >= minK)  # Having condition for total strikeouts
        )
    return query

# All players with 30 HR/ 30 SB season
# Parameters:
# Notes: 
def getPlayer3030Season():
    query = (db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
            .group_by(Batting.playerID, Batting.yearID)
            .having(
            and_(
                func.sum(Batting.b_HR) >= 30.0,
                func.sum(Batting.b_SB) >= 30.0
            )
        )
    )

    return query

# All players n+ Home Runs in a season
# Parameters: minHR - the number of home runs required
# Notes: 
def getPlayerSeasonHR(minHR):
    query = (db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
            .group_by(Batting.playerID, Batting.yearID)
            .having(
                func.sum(Batting.b_HR) >= minHR,
        )
    )
    return query

# All players n+ Career HR
# Parameters: minHR - the number of home runs required
# Notes: 
def getPlayerCareerHR(minHR):
    query = (db.session.query(
            Batting.playerID.label("playerID")
            )
            .group_by(Batting.playerID)
            .having(
                func.sum(Batting.b_HR) >= minHR,
        )
    )
    return query

# All players n+ Season Hits
# Parameters: minHits - the number of hits required
# Notes: 
def getPlayerSeasonHits(minHits):
    query = (db.session.query(
            Batting.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
            .group_by(Batting.playerID, Batting.yearID)
            .having(
                func.sum(Batting.b_H) >= minHits,
        )
    )
    return query

# All players n+ Career Hits
# Parameters: minHits - the number of hits required
# Notes: 
def getPlayerCareerHits(minHits):
    query = (db.session.query(
            Batting.playerID.label("playerID")
            )
            .group_by(Batting.playerID)
            .having(
                func.sum(Batting.b_H) >= minHits,
        )
    )
    return query

# All players who were in an all star game
# Parameters: 
# Notes: 
def getPlayerAllStar():
    query = (db.session.query(
            AllStarFull.playerID.label("playerID"),
            AllStarFull.teamID.label("teamID")
            )
    )
    return query

# All players who have recieved an award
# Parameters:
#    awardName: the name of the award
def getPlayerAward(awardName):
    query = (db.session.query(
            Awards.playerID.label("playerID"),
            Batting.teamID.label("teamID")
            )
            .join(Batting, and_(Awards.yearID == Batting.yearID, Awards.playerID == Batting.playerID))
            .filter(Awards.awardID == awardName)
    )
    return query

# Pitched min. 1 game
def getPitchers():
    query = (db.session.query(
            Pitching.playerID.label("playerID"),
            Pitching.teamID.label("teamID")
            )
            .filter(Pitching.p_G >= 1)
    )
    return query

# Played fielding position min. 1 game
def getFieldingPosition(position):
    query = (db.session.query(
            Fielding.playerID.label("playerID"),
            Fielding.teamID.label("teamID")
            )
            .filter(
                and_(Fielding.f_G >= 1, Fielding.position == position)
                )
    )
    return query

# Gets players who were born outside of the US
def getNonUSBirthCountry():
    return (
        db.session.query(
            People.playerID.label("playerID")
        )
        .filter(People.birthCountry != "USA")
    )

# Gets all players who have only played on one team
def getOneTeamPlayers():
    return (
        db.session.query(
            Batting.playerID.label("playerID"),
        )
        .join(Team, (Team.teamID == Batting.teamID))
        .group_by(Batting.playerID)
        .having(func.count(func.distinct(Batting.teamID)) == 1)
    )

# Solves the "immaculate grid" by processing queries for players matching specific criteria.
# Parameters:
# - questions (list[str]): A list of questions for the grid.
#   Questions can be team names, win thresholds (e.g., "10+ Win Season"), or other formats.
# Process:
# - Column Queries: Answers related to the top of the grid (first three questions).
# - Row Queries: Answers related to the side of the grid (last three questions).
# - Matching players are determined by finding intersections between column and row query results.
# Notes:
# - Players are added to the final result only once, avoiding duplicates using the `seenPlayers` set.
# Debug:
# - Outputs the team list, questions received, and debug details for each matching player.
# Returns: A list of full names for players who satisfy the grid criteria.
def solveGrid(questions):
    print("Questions received:", questions)  # Debug input

    columnQueries = [] # This will stores all the query results that apply to the column questions, i.e. everything on top of the grid
    rowQueries = [] # Same as above, but for every question on the side of the grid, the row questions.
   
    teamList = getAllTeams() # Just all the team names in the database
    #print("Team List:", teamList)  # Debug team mapping

    for index, currentQuestion in enumerate(questions):

        if currentQuestion in teamList: # If the player needs to be a part of a particular team
            subquery = getPlayersByTeam(currentQuestion.strip())
        elif ".300+ AVG Career Batting" in currentQuestion:
            subquery = getPlayerAvgByCareer()
        elif "Win Season" in currentQuestion: # If any n+ Win Season
            num = int(currentQuestion.partition("+")[0]) # Retrieves the minimum number of wins required
            subquery = getPlayerWinsBySeason(num)
        elif "AVG Season" in currentQuestion:
            subquery = getPlayerAvgBySeason()
        elif "Save Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerSVBySeason(num)
        elif "K Career" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerKByCareer(num)
        elif "Wins Career" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerCareerWins(num)
        elif "≤ 3.00 ERA Career" in currentQuestion:
            num = 3.0
            subquery = getPlayerCareerEra(num)
        elif "100+ RBI Season" in currentQuestion:
            num = 100
            subquery = getPlayerSeasonRBI(num)
        elif "+ K Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerSeasonK(num)
        elif "30+ HR / 30+ SB Season" in currentQuestion:
            subquery = getPlayer3030Season()
        elif "SB Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerSeasonSB(num)
        elif "+ HR Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerSeasonHR(num)
        elif "+ HR Career" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerCareerHR(num)
        elif "+ Hits Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerSeasonHits(num)
        elif "+ Hits Career" in currentQuestion:
            num = int(currentQuestion.partition("+")[0]) 
            subquery = getPlayerCareerHits(num)
        elif "WAR Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerWARSeason(num)
        elif "WAR Career" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            subquery = getPlayerWARCareer(num)
        elif "Pitched min. 1 game" in currentQuestion:
            subquery = getPitchers()
        elif "Played First Base min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("1B")
        elif "Played Second Base min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("2B")
        elif "Played Third Base min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("3B")
        elif "Played Shortstop min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("SS")
        elif "Played Catcher min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("C")
        elif "Played Right Field min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("RF")
        elif "Played Center Field min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("CF")
        elif "Played Left Field min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("LF")
        elif "Played Outfield min. 1 game" in currentQuestion:
            subquery = getFieldingPosition("OF")
        elif "Designated Hitter" in currentQuestion:
            subquery = getPlayerDesignatedHitter()
        elif "All Star" in currentQuestion:
            subquery = getPlayerAllStar()
        elif "Only One Team" in currentQuestion:
            subquery = getOneTeamPlayers()
        elif "Gold Glove" in currentQuestion:
            subquery = getPlayerAward("Gold Glove")
        elif "MVP" in currentQuestion:
            subquery = getPlayerAward("Most Valuable Player")
        elif "Silver Slugger" in currentQuestion:
            subquery = getPlayerAward("Silver Slugger")    
        elif "Cy Young" in currentQuestion:
            subquery = getPlayerAward("Cy Young Award")   
        elif "Rookie Of The Year" in currentQuestion:
            subquery = getPlayerAward("Rookie Of The Year Award") 
        elif "World Series Champ" in currentQuestion:
            subquery = getWorldSeriesChamp()
        else:
            print("ERROR: INVALID QUESTION!!!!")
            #Create a subquery type that won't return anything
            subquery= db.session.query(
                literal_column('TRUE').label('INVALID_QUESTION'),
                Batting.playerID 
            ).filter(Batting.b_G ==-1)

        # Any other question prompts should follow the format above. Any numeric prompts should function like the
        # win season and be capable of accepting any numeric value.

        if index < 3:
            columnQueries.append(subquery)
        else:
            rowQueries.append(subquery)


    finalPlayers = []

    # This builds the combined queries for each question combination
    # This should not need to be modified even if other questions are added.
    for rowQuery in rowQueries:
        for colQuery in columnQueries:         

            rowSubquery = rowQuery.subquery()  # Convert rowQuery to subquery
            colSubquery = colQuery.subquery()  # Convert colQuery to subquery
            combined = (
                db.session.query(Appearances.playerID)
                #Rules for joining the queries:
                # Always join on player ID
                # Join on teamId, IF...
                # Both subqueries have teamID attributes
                # AND ONE, BUT NOT BOTH subqureries have 'isTeamCheck' attributes (indicating it was a team name question)
                .join(
                    rowSubquery, 
                    and_(
                        Appearances.playerID == rowSubquery.c.playerID,
                        (rowSubquery.c.teamID == Appearances.teamID) if hasattr(rowSubquery.c, 'teamID')else True  
                        # Join on teamID if it exists in rowSubquery
                    )
                )
                .join(
                    colSubquery,
                    and_(
                        rowSubquery.c.playerID == colSubquery.c.playerID,
                        (colSubquery.c.teamID == rowSubquery.c.teamID) 
                        if hasattr(colSubquery.c, 'teamID') #Must both have teamID
                        and hasattr(rowSubquery.c, 'teamID') #Must both have teamID
                        #At least one must have the team check
                        and (hasattr(rowSubquery.c, 'isTeamCheck') or hasattr(colSubquery.c,"isTeamCheck") )
                        #but not both
                        and not(hasattr(rowSubquery.c, 'isTeamCheck') and hasattr(colSubquery.c,"isTeamCheck") )
                        else True  
                        # Join on teamID if it exists in colSubquery
                    )
                )
                .group_by(Appearances.playerID,Appearances.teamID)
                .order_by(Appearances.G_all)
                .limit(1)
            ).first()
            
            if combined:

                # Fetch the full name of the selected player.
                player = (
                    db.session.query(People.nameFirst, People.nameLast)
                    .filter(People.playerID == combined.playerID)
                    .first()
                )
                if player:
                    fullName = f"{player.nameFirst} {player.nameLast}"
                    finalPlayers.append(fullName)
                    print(f"Added player for grid cell: {fullName}")  # Debug.
                else:
                    print("Could not find valid player!")
                    finalPlayers.append("No player found!")
            else:
                print("Could not find valid player!")
                finalPlayers.append("No player found!")


    print("Final Players:", finalPlayers)  # Ensure final list is correct

    return finalPlayers

                    
            

