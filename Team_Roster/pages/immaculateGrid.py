from flask import render_template, request
from app.forms import ImmaculateGridInput

def ShowImmaculateGrid():
    form = ImmaculateGridInput()
    url= ""
    questions = None
    solutionNames = None

    if form.validate_on_submit():
        url = form.url.data
        questions = ["Detroit Tigers","Boston Red Sox","Season RBI 500+","World Series Winner", "Seattle Mariners", "Played 1st Base +1 Game"]
        solutionNames = ["Babe Ruth", "Also Babe Ruth","Babe Ruth Once Again",
                         "Logan Rigdon","Samuel Fries","August Rothpletz",
                         "Mitchell Thompson","Uhhhhhh Speegle","500 Cent Ice Tea DOOM"]

        
    
    return render_template('immaculateGrid.html', title='Immaculate Grid Solver', form=form, url = url,questions = questions, solutionNames = solutionNames)