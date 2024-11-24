from flask import jsonify, render_template, request
from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Batting, Team, Pitching, Season
from sqlalchemy import func, and_


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
        db.session.query(People.playerID)
        .select_from(Team)
        .join(Batting, (Batting.teamID == Team.teamID) & (Batting.yearID == Team.yearID))
        .join(People, Batting.playerID == People.playerID)
        .filter(Team.team_name == team_name)
        .group_by(People.playerID)
        .subquery()
        .select()
    )


# Retrieves all players who have achieved a minimum number of wins in a season.
# Parameters:
# - numWins (int): The minimum number of wins required.
# Notes: 
# - Only pitchers are awarded "wins," as this statistic is specific to the Pitching table.
# - The query joins People, Pitching, and Team tables to ensure accurate filtering and grouping.
def getPlayerWinsBySeason(numWins):
    return (
        db.session.query(People.playerID)
        .join(Pitching, People.playerID == Pitching.playerID)
        .join(Team, (Team.yearID == Pitching.yearID) & (Team.teamID == Pitching.teamID))
        .filter(Pitching.p_W >= numWins)
        .group_by(People.playerID)
        .subquery()
        .select()
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

        elif "Win Season" in currentQuestion: # If any n+ Win Season
            num = int(currentQuestion.partition("+")[0]) # Retrieves the minimum number of wins required
            subquery = getPlayerWinsBySeason(num)
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
    for colQuery in columnQueries:
        for rowQuery in rowQueries:            
            combined = (
                db.session.query(People.playerID)
                .filter(People.playerID.in_(colQuery))
                .filter(People.playerID.in_(rowQuery))
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


    print("Final Players:", finalPlayers)  # Ensure final list is correct

    return finalPlayers

                    
            

