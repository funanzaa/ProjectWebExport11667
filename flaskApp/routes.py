from flask import render_template, url_for, flash, redirect, request, abort, jsonify, make_response
from flaskApp.forms import  LoginForm
from flaskApp import app
from flaskApp.models import Student
from flaskApp.database import Database
# import psycopg2
# import psycopg2.extras

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]



@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html',title='Home' , posts=posts)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'demo':
            # flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            pass
    return render_template('login.html', title='Login', form=form)

# HighCost
@app.route("/highCost" , methods=['GET', 'POST'])
def highCost():
    db = Database()
    list_Item = db.selectItem()
    return render_template('highcost.html',title='รายการ NHSO High Cost', list_Items = list_Item)

# Update HighCost
@app.route("/highCostID/" , methods=['GET', 'POST'])
def highCostID():
    db = Database()
    
    req = request.get_json()
    
    _id = req.get('id')
    _status = req.get('status')

    db.updateHighCost(_id, _status)

    res = make_response(jsonify({"message":"JSON received"}), 200)
        
    return res

# ./ HighCost

#  contactPlan
@app.route("/contactPlan")
def contactPlan():
    db = Database()
    list_plan = db.selectPlan()
    return render_template('contact_plan.html',title = 'จับคู่สิทธิ์การรักษา', list_plans = list_plan)

@app.route("/edit_contactPlan/<id>", methods=['GET', 'POST'])
def edit_contactPlan(id):
    db = Database()
    list_optype = db.selectOPTYPE()
    descPlan = db.selectDescPlan(id)
    if request.method == 'POST':
        id_optype = request.form["optype"]
        db.updatePlan(id_optype, id)
        list_plan = db.selectPlan()
        return redirect(url_for('contactPlan'))
    return render_template('edit_contactPlan.html',title = 'จับคู่สิทธิ์การรักษา', list_optypes = list_optype, descplans = descPlan[0][0], id_plan = descPlan[0][1])

# map base_billing_group
@app.route("/billing_group/", methods=['GET', 'POST'])
def billing_group():
    db = Database()
    list_Item_opd = db.selectBillingGroupOPD()
    list_Item_ipd = db.selectBillingGroupIPD()
    return render_template('billing_group.html',title='ใบเสร็จการรักษา', list_Items = list_Item_opd, list_ItemsIPD = list_Item_ipd )

@app.route("/edit_billing_group/<id>", methods=['GET', 'POST'])
def edit_billing_group(id):
    db = Database()
    list_Chrgitem = db.selectMapChrgitem()
    list_ChrgitemEdit = db.selectBillingEdit(id)
    if request.method == 'POST':
        id_chrgitem = request.form["chrgitem"]
        db.UpdateBillingGroup(id_chrgitem, id)
        return redirect(url_for('billing_group'))
    return render_template('pages/edit_billing_group.html',title = 'ใบเสร็จการรักษา', list_Chrgitems = list_Chrgitem,list_ChrgitemEdits = list_ChrgitemEdit)

@app.route("/delete_billing_group/<id>", methods=['GET', 'POST'])
def delete_billing_group(id):
    db = Database()
    db.UpdateBillingGroup('', id)
    return redirect(url_for('billing_group'))
