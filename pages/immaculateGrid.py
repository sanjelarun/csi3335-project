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
    solution = None

    if form.validate_on_submit():
        url = form.url.data
        questions = scrapeImmaculateGridQuestions(url)
        if(form.solveCheckbox.data):
            solution = solveOptimalGrid(url)
        else:
            solution = solveGrid(questions)
        for i in range(3):  # 3 rows
            for j in range(3):  # 3 columns
                q_questions = questions[j] + " & " + questions[i + 3]
                q_solutions = solution[i * 3 + j]

                query = Queries(user_ID=current_user.get_id(), q_QUESTIONS=q_questions, q_SOLUTIONS=q_solutions)
                db.session.add(query)
                db.session.commit()

        for i in range(3):  # 3 rows
            for j in range(3):  # 3 columns
                q_questions = questions[j] + " & " + questions[i + 3]
                q_solutions = solution[i * 3 + j]

                query = Queries(user_ID=current_user.get_id(), q_QUESTIONS=q_questions, q_SOLUTIONS=q_solutions)
                db.session.add(query)
                db.session.commit()

        print("URL:", url)
        print("Questions:", questions)
        ("Solution:", solution)

    return render_template('immaculateGrid.html', title='Immaculate Grid Solver', form=form, url = url,questions = questions, solution = solution)