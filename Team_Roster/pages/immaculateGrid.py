from flask import render_template, request
from app.forms import ImmaculateGridInput
from immaculateGridCalculations.webScraper import scrapeImmaculateGridQuestions, solveGridWeb
from immaculateGridCalculations.gridSolver import solveGrid

def ShowImmaculateGrid():
    form = ImmaculateGridInput()
    url= ""
    questions = None
    solutionNames = None

    if form.validate_on_submit():
        url = form.url.data
        questions = scrapeImmaculateGridQuestions(url)

        if(form.solveCheckbox.data):
            solutionNames = solveGridWeb(url)
        else:
            solutionNames = solveGrid(questions)

        print("URL:", url)
        print("Questions:", questions)
        ("Solution Names:", solutionNames)
    
    return render_template('immaculateGrid.html', title='Immaculate Grid Solver', form=form, url = url,questions = questions, solutionNames = solutionNames)