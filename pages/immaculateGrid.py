from flask import render_template, request
from flask_login import current_user
from app.forms import ImmaculateGridInput
from immaculateGridCalculations.webScraper import scrapeImmaculateGridQuestions, solveOptimalGrid
from immaculateGridCalculations.gridSolver import solveGrid

from app.models import Queries
from app import db


def ShowImmaculateGrid():
    form = ImmaculateGridInput()
    url = ""
    questions = None
    solutionNames = None

    if form.validate_on_submit():
        url = form.url.data
        questions = scrapeImmaculateGridQuestions(url)

        if(form.solveCheckbox.data):
            solutionNames = solveOptimalGrid(url)
        else:
            solutionNames = solveGrid(questions)

        for i in range(3):  # 3 rows
            for j in range(3):  # 3 columns
                q_questions = questions[j] + " & " + questions[i + 3]
                q_solutions = solutionNames[i * 3 + j]

                query = Queries(user_ID=current_user.get_id(), q_QUESTIONS=q_questions, q_SOLUTIONS=q_solutions)
                db.session.add(query)
                db.session.commit()

        print("URL:", url)
        print("Questions:", questions)
        ("Solution Names:", solutionNames)

    return render_template('immaculateGrid.html', title='Immaculate Grid Solver', form=form, url=url,
                           questions=questions, solutionNames=solutionNames)