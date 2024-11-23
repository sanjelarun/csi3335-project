from flask import jsonify, render_template, request
from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Batting, Team, Pitching, Season
from sqlalchemy import func, and_


def getAllTeams():
    teams = db.session.query(Team.team_name).all() 
    team_list = [team.team_name for team in teams]
    return team_list


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
    return players.all()


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



def solveGrid(questions):
    print("Questions received:", questions)  # Debug input

    columnQueries = []
    rowQueries = []
    queryAnswers = []
    seenPlayers = set()

    teamList = getAllTeams()
    print("Team List:", teamList)  # Debug team mapping

    for currentQuestion in questions:
        if currentQuestion in teamList:
            queryAnswers.append(getPlayersByTeam(currentQuestion.strip()))

        if "Win Season" in currentQuestion:
            num = int(currentQuestion.partition("+")[0])
            queryAnswers.append(getPlayerWinsBySeason(num))

    print("Query Answers Length:", len(queryAnswers))  # Ensure 6 queries are generated


    columnQueries = queryAnswers[:3]
    rowQueries = queryAnswers[3:]

    finalPlayers = []

    for colQuery in columnQueries:
        columnPlayers = {player.playerID for player in colQuery}
        for rowQuery in rowQueries:
            rowPlayers = {player.playerID for player in rowQuery}
            
            matching = columnPlayers & rowPlayers
            matching -= seenPlayers

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

                    
            

