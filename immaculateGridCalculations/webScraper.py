import requests
import re
import json
import unicodedata
from datetime import datetime
from bs4 import BeautifulSoup

def scrapeImmaculateGridQuestions(url):
    # Make a request for the HTML info
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Fetches the question elements that we need based on HTML data
    s = soup.find('div',
                  class_='bg-white dark:bg-gray-800 rounded-xl border dark:border-gray-950 grid grid-cols-3 overflow-hidden')

    # Get the HTML attributes that store the question information
    content = s.find_all('button')

    #Storing in two different lists in order to get the correct question order
    questionsCol = []
    questionsRow = []
    for e in content:
        # Split the questions and append to the questions array
        print(str(e.attrs['aria-label']))
        questionStr = str(e.attrs['aria-label']).split(" + ", 1)
        # print(str(e.attrs['aria-label']).split(" + ", 1))

        rowQuestion = prepQuestionString(questionStr[0])
        if rowQuestion not in questionsRow:
            questionsRow.append(rowQuestion)
        columnQuestion = prepQuestionString(questionStr[1])
        if columnQuestion not in questionsCol:
            questionsCol.append(columnQuestion)
    # questions = ["Detroit Tigers","200+ K Season","≤ 3.00 ERA Career","Gold Glove", "Played First Base min. 1 game", "Houston Astros"]
    # return questions
    # Remove duplicates from both sets, append into questionsCol, giving columns precedence
    questionsCol = list(questionsCol)
    questionsCol += list(questionsRow)

    return questionsCol

def prepQuestionString(questionStr):
    str = questionStr.rstrip() #remove trailing whitespace
    # remove repeated spaces
    str = re.sub(r'\s{2,}', ' ', str)
    return str

# Returns a JSON table to be used in a POST request to the immaculate grid.
# Parameters:
#   - (str) gridNum : The grid ID to fetch
# Returns:
#   - The completed JSON for the specified grid
def loadGrid(gridNum: str) -> list:
    # Making a GET request
    r = requests.get('https://api.sports-reference.com/v1/br/grids')
    localStorageKey = None
    grids = list(json.loads(r.text)['grids'])

    # If gridNum is empty, use the current grid. Requesting the actual website is the only solution.
    if(len(gridNum) == 0):
        r = requests.get('https://www.immaculategrid.com/')
        localStorageKey = r.text[r.text.find("localStorageKey")+20:r.text.find("localStorageKey")+33]
    else:
        for x in grids:
            if x['gridId'] == gridNum:
                localStorageKey = x['localStorageKey']
                break
    jsonTable = {
        "gridKey": localStorageKey,
        "correctAnswers": [
            [None, None, None], [None, None, None], [None, None, None]
        ]
    }
    return jsonTable

# This looks like spaghetti, but it minimizes the score until no duplicates exist.
# Parameters:
#   - dupes: list containing indices of duplicate values related to bestAnswers
#   - scoreList: the score table to get the values from
#   - bestAnswers: the list containing the current best answers
# Returns:
#   - None
def pickNextLowestPlayer(dupes, scoreList, bestAnswers):
    for item in dupes:
        while(len(item)>1): # Until no duplicates exist in each square
            # Find the next lowest score of both squares that are equal
            optimizeFirst = min(scoreList[item[0]], key=scoreList[item[0]].get)
            optimizeSecond = min(scoreList[item[1]], key=scoreList[item[1]].get)

            # If the player found was already picked in the current solution,
            # skip that player and redo
            if (optimizeFirst in dict(bestAnswers).keys()):
                item.pop(0)
                continue
            elif (optimizeSecond in dict(bestAnswers).keys()):
                item.pop(1)
                continue

            # Compare the scores of the two new players found.
            # If the two players have equal scores, go with the first
            if scoreList[item[0]][optimizeFirst]<= scoreList[item[1]][optimizeSecond]:
                bestAnswers[item[0]] = [optimizeFirst, scoreList[item[0]][optimizeFirst]]
                del scoreList[item[0]][optimizeFirst] # Remove player from being pulled
                item.pop(0)
            elif scoreList[item[0]][optimizeFirst]> scoreList[item[1]][optimizeSecond]:
                bestAnswers[item[1]] = [optimizeSecond, scoreList[item[1]][optimizeSecond]]
                del scoreList[item[1]][optimizeFirst] # Remove player from being pulled
                item.pop(1)

# Gets the best answers for the given table according to the immaculate grid.
# Parameters:
#   - (list) jsonTable: The ordered list containing the relevant grid information for the request
# Returns:
#   - A list containing the best possible player answers as playerIDs
def getBestAnswers(jsonTable: list) -> list:
    getScore = requests.post('https://www.immaculategrid.com/api/score', json=jsonTable)
    scoreList = getScore.text.split("correctAnswersPlayerMap\":")
    scoreList = (scoreList[1].split("}}")[0])  # Truncate irrelevant information
    bestAnswers = []
    scoreList = json.loads(scoreList)  # Format into usable JSON
    scoreList = scoreList[0] + scoreList[1] + scoreList[2]
    dupes = []

    for i in scoreList:
        # Insert the lowest scoring player into ordered list
        plr = min(i, key=i.get)
        bestAnswers.append([plr, i[plr]])
        dupes.append([i for i, x in enumerate(bestAnswers) if x[0] == plr])
        del i[plr] # Remove the inserted player to prevent duplicate pulls later
    pickNextLowestPlayer(dupes, scoreList, bestAnswers)
    return bestAnswers


# Gets the player information based on their player ID
# Parameters:
#   - (list) answerDict: An ordered list containing player IDs
# Returns:
#   - A list containing player information of the given players
def getPlayerAnswers(playerList: list) -> list:
    answers = []
    for player in playerList:
        r = requests.get('https://api.sports-reference.com/v1/br/players/' + player[0])
        playerJSON = json.loads(r.text)
        # Prepend the baseball reference URL to the player image path
        if('headshot_url' in playerJSON):
            playerJSON['headshot_url'] = "https://www.baseball-reference.com/req/" + playerJSON['headshot_url']
        # answers.insert(i, playerJSON)
        answers.append(unicodedata.normalize('NFKD',  playerJSON['name']+' ('+playerJSON['years']+')').encode('ascii', 'ignore').decode("utf-8"))
    return answers

def solveGridWeb(url: str)-> list:
    gridNum = url[url.find("grid-") + 5:]
    if(url.find("grid-") == -1 or not gridNum.isnumeric()):
        gridNum = ''
    return (getPlayerAnswers(getBestAnswers(loadGrid(gridNum))))
