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
    # questions = ["30+ HR Season Batting","World Series Champ","","Toronto Blue Jays", "", ""]
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