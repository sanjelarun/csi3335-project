from flask import render_template, url_for, redirect
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
    return queries

def getImmaculateGridQueries(user_id):
    queries = db.session.query(Queries).filter(
        and_(
            Queries.user_ID == user_id,
            Queries.q_TEAM == None,
            Queries.q_YEAR == None
        )
    ).all()
    return queries

def DeleteRosterQueries(user_id):
    rosterQueryData = getRosterQueries(user_id)
    if rosterQueryData:
        for query in rosterQueryData:
            db.session.delete(query)
        db.session.commit()
    return redirect(url_for('main.queries'))

def DeleteImmaculateGridQueries(user_id):
    immaculateGridQueryData = getImmaculateGridQueries(user_id)
    if immaculateGridQueryData:
        for query in immaculateGridQueryData:
            db.session.delete(query)
        db.session.commit()
    return redirect(url_for('main.queries'))