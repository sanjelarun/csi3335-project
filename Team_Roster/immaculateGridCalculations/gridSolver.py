from flask import jsonify, render_template, request
from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Batting, Team, Pitching, Season
from sqlalchemy import func, and_, literal_column


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

# All players with a CAREER era over a certian amount
# Parameters:
# - numWins (int): The minimum career ERA required
# Notes: 
# - Career ERA cannot be caluclated using stint ERA, so I had to do the full calculaton
def getPlayerCareerEra(greaterThan):
    return (
        db.session.query(Pitching.playerID.label("playerID"))
        .group_by(Pitching.playerID)
        .having(#Career ERA = Career ER / (Career IPOuts/3) * 9
            (
                func.sum(Pitching.p_ER)
                /
                (func.sum(Pitching.p_IPOuts)/3)
                *9
            ) >= greaterThan
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
def getPlayerSeasonK(minK,teamName):
    query = (
        db.session.query(
            Pitching.playerID,
            Pitching.teamID.label("teamID")
        )
        .group_by(Pitching.playerID, Pitching.yearID, Pitching.teamID)  # Group by playerID, yearId, and teamID
        .having(func.sum(Pitching.p_SO) >= 200)  # Having condition for total strikeouts
        )
    return query


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
        teamName=""

        if currentQuestion in teamList: # If the player needs to be a part of a particular team
            subquery = getPlayersByTeam(currentQuestion.strip())

        elif "Win Season" in currentQuestion: # If any n+ Win Season
            num = int(currentQuestion.partition("+")[0]) # Retrieves the minimum number of wins required
            subquery = getPlayerWinsBySeason(num)
        elif "≤ 3.00 ERA Career" in currentQuestion:
            num = 3.0
            subquery = getPlayerCareerEra(num)
        elif "100+ RBI Season" in currentQuestion:
            num = 100
            subquery = getPlayerSeasonRBI(num,teamName)
        elif "200+ K Season" in currentQuestion:
            num = 200
            subquery = getPlayerSeasonK(num,teamName)
        else:
            continue

        # Any other question prompts should follow the format above. Any numeric prompts should function like the
        # win season and be capable of accepting any numeric value.

        if index < 3:
            columnQueries.append(subquery)
        else:
            rowQueries.append(subquery)


    finalPlayers = []

    # This builds the combined queries for each question combination
    # This should not need to be modified even if other questions are added.
    for id,rowQuery in enumerate(rowQueries):
        for jd,colQuery in enumerate(columnQueries):           
            # print(f"Row Query: {questions[id+3]}")
            # print(f"Col Query: {questions[jd]}")

            rowSubquery = rowQuery.subquery()  # Convert rowQuery to subquery
            colSubquery = colQuery.subquery()  # Convert colQuery to subquery
            combined = (
                db.session.query(Batting.playerID)
                .join(
                    rowSubquery, 
                    and_(
                        Batting.playerID == rowSubquery.c.playerID,
                        (rowSubquery.c.teamID == Batting.teamID) if hasattr(rowSubquery.c, 'teamID')else True  
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
                    finalPlayers.append(f"{questions[id+3]} {questions[jd]} "+fullName)
                    print(f"Added player for grid cell: {fullName}")  # Debug.
                else:
                    print("Could not find valid player!")
                    finalPlayers.append("No player found!")
            else:
                print("Could not find valid player!")
                finalPlayers.append("No player found!")


    print("Final Players:", finalPlayers)  # Ensure final list is correct

    return finalPlayers

                    
            

