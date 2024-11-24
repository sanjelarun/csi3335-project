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
# Parameters:
# - team_name (str): The name of the team to query.
# Returns: A list of tuples, where each tuple contains a player's ID and the team name.
# Notes: The query ensures that players are grouped by their playerID and the team's name.
# Debug: Outputs the team being queried and the total count of players found.
def getPlayersByTeam(team_name):
    print(f"Querying team: {team_name}")
    players = (
        db.session.query(People.playerID, Team.team_name)
        .select_from(Team)
        .join(Batting, (Batting.teamID == Team.teamID) & (Batting.yearID == Team.yearID))
        .join(People, Batting.playerID == People.playerID)
        .filter(Team.team_name == team_name)
        .group_by(People.playerID, Team.team_name)
    )
    print(f"Players found for {team_name}: {players.count()}")
    return players.all() # the .all() returns the answers to the query


# Retrieves all players who have achieved a minimum number of wins in a season.
# Parameters:
# - numWins (int): The minimum number of wins required.
# Returns: A list of playerIDs that satisfy the criteria.
# Notes: 
# - Only pitchers are awarded "wins," as this statistic is specific to the Pitching table.
# - The query joins People, Pitching, and Team tables to ensure accurate filtering and grouping.
# Debug: Outputs the number of players found with the required wins.
def getPlayerWinsBySeason(numWins):
    print(f"Querying players with >= {numWins} wins")

    playerWins = (
        db.session.query(
            People.playerID
        )
        .join(Pitching, People.playerID == Pitching.playerID).join(Team, (Team.yearID == Pitching.yearID) & (Team.teamID == Pitching.teamID))
        .filter(Pitching.p_W >= numWins)
        .group_by(People.playerID)
    )
    print(f"Players found with >= {numWins} wins: {playerWins.count()}")

    return playerWins.all() 


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
    queryAnswers = [] # This will store all query answers
    seenPlayers = set() # This will be used to ensure each player is only seen once

    teamList = getAllTeams() # Just all the team names in the database
    print("Team List:", teamList)  # Debug team mapping

    for currentQuestion in questions:
        if currentQuestion in teamList: # If the player needs to be a part of a particular team
            queryAnswers.append(getPlayersByTeam(currentQuestion.strip()))

        elif "Win Season" in currentQuestion: # If any n+ Win Season
            num = int(currentQuestion.partition("+")[0]) # Retrieves the minimum number of wins required
            queryAnswers.append(getPlayerWinsBySeason(num))

        # Any other question prompts should follow the format above. Any numeric prompts should function like the
        # win season and be capable of accepting any numeric value.

    print("Query Answers Length:", len(queryAnswers))  # Ensure 6 queries are generated


    columnQueries = queryAnswers[:3] # queryAnswers 1-3 are always associated with the columns
    rowQueries = queryAnswers[3:] # queryAnswers 4-6 are always rows

    finalPlayers = []

    for colQuery in columnQueries:
        columnPlayers = {player.playerID for player in colQuery}
        for rowQuery in rowQueries:
            rowPlayers = {player.playerID for player in rowQuery} # This gets the playerid for every player in each query
            
            matching = columnPlayers & rowPlayers # This finds the intersection between the column answers and row answer(i.e. common players)
            matching -= seenPlayers # If the player has already been calculated for the final result, it does not get rechecked

            if matching:
                selectedPlayer = next(iter(matching))
                seenPlayers.add(selectedPlayer)

                player = (
                    db.session.query(
                        People.nameFirst,
                        People.nameLast
                    )
                    .filter(People.playerID == selectedPlayer)
                    .first()
                )
                if player:
                    fullName = f"{player.nameFirst} {player.nameLast}"
                    finalPlayers.append(fullName)
                    print("Added player:", fullName)



    # result = (
    #     db.session.query(People.nameFirst, People.nameLast)
    #     .filter(People.playerID.in_(resultPlayers))
    #     .all()
    # )
    print("Final Players:", finalPlayers)  # Ensure final list is correct

    return finalPlayers

                    
            

