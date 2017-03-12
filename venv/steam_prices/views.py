from flask import render_template, flash, redirect
from steam_prices import app, my_price_checker
from .forms import SteamItemForm
from urllib.parse import unquote


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def item_check():
    user = {'nickname': 'Rusty'}  # fake user
    
    form = SteamItemForm()
    if form.validate_on_submit():
        parsed_item=unquote(form.item_name.data)
        flash('Prices requested for Item="%s"' %
              (parsed_item))
        
        days = form.days.data if form.days.data is not None else 14
        
        default_days = [1,3,7,14,30,90]
        
        # custom days
        if days not in default_days:
            default_days.insert(0,days)
            
        days_list=[]
        for i in default_days:
            days_list.append(
                "".join(
                    [
                        "Price over last {} days<br>".format(i),
                        my_price_checker.get_item_history(form.item_name.data,days=i).to_html().replace('class="dataframe"','class="hor-minimalist-b"')
                    ]
                )
            )
        


        output_list  = "<br>".join(days_list)
        
        result_data ={
            "form":form,
            "user":user,
            "output_list":output_list,
            "parsed_item":parsed_item
        }
        
        return render_template("result.html",
                            title="Results for {}".format(parsed_item),
                            result_data=result_data
                            )
                            
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