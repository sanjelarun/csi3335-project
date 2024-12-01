import requests
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
        questionStr = str(e.attrs['aria-label']).split(" + ", 1)
        # print(str(e.attrs['aria-label']).split(" + ", 1))
        questionsRow.append(questionStr[0].rstrip())
        questionsCol.append(questionStr[1].rstrip())
    # questions = ["Detroit Tigers","200+ K Season","≤ 3.00 ERA Career","Gold Glove", "Played First Base min. 1 game", "Houston Astros"]
    # Remove duplicates from both sets, append into questionsCol, giving columns precedence
    questionsCol = list(set(questionsCol))
    questionsCol += list(set(questionsRow))
    return questionsCol
