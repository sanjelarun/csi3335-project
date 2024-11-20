from flask import render_template, request
from app.forms import ImmaculateGridInput
from immaculateGridCalculations.webScraper import scrapeImmaculateGridQuestions
from immaculateGridCalculations.gridSolver import solveGrid

def ShowImmaculateGrid():
    form = ImmaculateGridInput()
    url= ""
    questions = None
    solutionNames = None

    if form.validate_on_submit():
        url = form.url.data
        questions = scrapeImmaculateGridQuestions(url)
        solutionNames = solveGrid(questions)
    
    return render_template('immaculateGrid.html', title='Immaculate Grid Solver', form=form, url = url,questions = questions, solutionNames = solutionNames)