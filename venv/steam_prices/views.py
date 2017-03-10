from flask import render_template, flash, redirect
from steam_prices import app
from .forms import SteamItemForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def item_check():
    user = {'nickname': 'Rusty'}  # fake user
    
    form = SteamItemForm()
    if form.validate_on_submit():
        flash('Prices requested for Item="%s"' %
              (form.item_name.data))
        
       
        
        return render_template("result.html",
                            form=form,
                            title="Results",
                            user = user)
                            
    else:
        return render_template('item_check.html', 
                           title='Item Prices',
                           form=form)
                           
@app.route("/result")

def result():
    
    user = {'nickname': 'Rusty'}  # fake user
    
    return render_template("result.html",
                           title='Home',
                           user=user
                           
                           )