from flask import render_template
from sqlalchemy import and_
from app.models import Queries
from app import db


def ShowQueries(user_id):
    rosterQueryData = getRosterQueries(user_id)
    immaculateGridQueryData = getImmaculateGridQueries(user_id)
    return render_template('queries.html',
                           rosterQueryData=rosterQueryData,
                           immaculateGridQueryData=immaculateGridQueryData)

def getRosterQueries(user_id):
    queries = db.session.query(Queries).filter(
        and_(
            Queries.user_ID == user_id,
            Queries.q_QUESTIONS == None,
            Queries.q_SOLUTIONS == None
        )
    ).all()
    print(f"Roster Queries for user {user_id}: {queries}")
    return queries

def getImmaculateGridQueries(user_id):
    queries = db.session.query(Queries).filter(
        and_(
            Queries.user_ID == user_id,
            Queries.q_TEAM == None,
            Queries.q_YEAR == None
        )
    ).all()
    print(f"Immaculate Grid Queries for user {user_id}: {queries}")
    return queries