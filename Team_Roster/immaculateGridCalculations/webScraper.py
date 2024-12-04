import requests
import re
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
    # Remove duplicates from both sets, append into questionsCol, giving columns precedence
    questionsCol = list(questionsCol)
    questionsCol += list(questionsRow)

    return questionsCol

def prepQuestionString(questionStr):
    str = questionStr.rstrip() #remove trailing whitespace
    # remove repeated spaces
    str = re.sub(r'\s{2,}', ' ', str)
    return str

import requests
import json


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
    for x in grids:
        if x['gridId'] == gridNum:
            localStorageKey = x['localStorageKey']
    # print(localStorageKey)
    jsonTable = {
        "gridKey": localStorageKey,
        "correctAnswers": [
            [None, None, None], [None, None, None], [None, None, None]
        ]
    }
    return jsonTable


# Gets the best answers for the given table according to the immaculate grid.
# Parameters:
#   - (list) jsonTable: The ordered list containing the relevant grid information for the request
# Returns:
#   - A list containing the best possible player answers as playerIDs
def getBestAnswers(jsonTable: list) -> list:
    getScore = requests.post('https://www.immaculategrid.com/api/score', json=jsonTable)
    scoreText = getScore.text.split("correctAnswersPlayerMap\":")
    scoreText = (scoreText[1].split("}}")[0])  # Truncate irrelevant information
    squareNum = 1 # Ensures list is ordered
    bestAnswers = []
    scoreText = json.loads(scoreText)  # Format into usable JSON

    for i in scoreText[0] + scoreText[1] + scoreText[2]:
        # Insert the lowest scoring player into ordered list
        bestAnswers.insert(squareNum, min(i, key=i.get))
        squareNum += 1
    return bestAnswers


# Gets the player information based on their player ID
# Parameters:
#   - (list) answerDict: An ordered list containing player IDs
# Returns:
#   - A list containing player information of the given players
def getPlayerAnswers(playerList: list) -> list:
    answers = []
    i = 1  # Ensures list is ordered
    for player in playerList:
        r = requests.get('https://api.sports-reference.com/v1/br/players/' + player)
        playerJSON = json.loads(r.text)
        # Prepend the baseball reference URL to the player image path
        playerJSON['headshot_url'] = "https://www.baseball-reference.com/req/" + playerJSON['headshot_url']
        # answers.insert(i, playerJSON) #USE THIS FOR EXTRA INFO
        answers.insert(i, playerJSON['name'])
        print(playerJSON['name'])
        i += 1  # Increment index
    return answers

def getAnswersForGrid(gridNum: str):
    return getPlayerAnswers(getBestAnswers(loadGrid(gridNum)))
