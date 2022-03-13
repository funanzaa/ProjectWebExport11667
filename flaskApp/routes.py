from flask import render_template, url_for, flash, redirect, request, abort, jsonify, make_response
from flaskApp.forms import  LoginForm, RegistrationForm
from flaskApp import app, db, bcrypt
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
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form= form)

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

@app.route("/delete_contactPlan/<id>", methods=['GET', 'POST'])
def delete_contactPlan(id):
    db = Database()
    db.deleteMapPlan(id)
    return redirect(url_for('contactPlan'))

# map base_billing_group
@app.route("/billing_group/", methods=['GET', 'POST'])
def billing_group():
    db = Database()
    list_Item_opd = db.selectBillingGroupOPD()
    list_Item_ipd = db.selectBillingGroupIPD()
    return render_template('billing_group.html',title='ใบเสร็จการรักษา', list_Items = list_Item_opd, list_ItemsIPD = list_Item_ipd )

@app.route("/edit_billing_group/<typename>/<id>", methods=['GET', 'POST'])
def edit_billing_group(typename, id):
    db = Database()
    list_Chrgitem = db.selectMapChrgitem()
    list_ChrgitemEdit = db.selectBillingEdit(id, typename)
    if request.method == 'POST':
        id_chrgitem = request.form["chrgitem"]
        db.UpdateBillingGroup(id_chrgitem, id, typename)
        return redirect(url_for('billing_group'))
    return render_template('pages/edit_billing_group.html',title = 'ใบเสร็จการรักษา', list_Chrgitems = list_Chrgitem,list_ChrgitemEdits = list_ChrgitemEdit,nameHeader = typename)

@app.route("/delete_billing_group/<typename>/<id>", methods=['GET', 'POST'])
def delete_billing_group(typename, id):
    db = Database()
    db.UpdateBillingGroup('', id, typename)
    return redirect(url_for('billing_group'))

# map lapfu
@app.route("/mapLapFu" , methods=['GET', 'POST'])
def mapLapFu():
    db = Database()
    list_Item = db.selectItemMapLapFu()
    return render_template('labfu.html',title='จับคู่ LabFu', list_Items = list_Item)


@app.route("/edit_mapLapFu/<id>", methods=['GET', 'POST'])
def edit_mapLapFu(id):
    db = Database()
    list_nhsoLabFu = db.selectItemNhsoLabFu()
    list_editLabFu = db.editNhsoLabFu(id)
    if request.method == 'POST':
        id_nhsoLabFu = request.form["idLabFu"]
        db.updateNhsoLabFu(id, id_nhsoLabFu)
        return redirect(url_for('mapLapFu'))
    return render_template('pages/edit_labfu.html',title = 'Nhso LabFu', list_nhsoLabFu = list_nhsoLabFu, list_editLabFu = list_editLabFu)

@app.route("/delete_mapLapFu/<id>", methods=['GET', 'POST'])
def delete_mapLapFu(id):
    db = Database()
    db.updateNhsoLabFu(id, '')
    return redirect(url_for('mapLapFu'))


#  FeeSchedule
@app.route("/ListFeeSchedule", methods=['GET', 'POST'])
def ListFeeSchedule():
    db = Database()
    ListFeeSchedule = db.ListFeeSchedule()
    return render_template('FeeSchedule.html',title = 'รายการ FeeSchedule', ListFeeSchedule = ListFeeSchedule)


@app.route("/ListMatchFeeSchedule", methods=['GET', 'POST'])
def ListMatchFeeSchedule():
    db = Database()
    ListIsMatchFeeSchedule = db.ListIsMatchFeeSchedule()
    ListNotMatchFeeSchedule = db.ListNotMatchFeeSchedule()
    return render_template('ListMatchFeeSchedule.html',title='จับคู่ FeeSchedule', list_Items = ListIsMatchFeeSchedule, ListNotMatchFeeSchedule = ListNotMatchFeeSchedule )


@app.route("/UpdateFeeSchedule/<id>", methods=['GET', 'POST'])
def UpdateFeeSchedule(id):
    db = Database()
    ListFeeSchedule = db.ListFeeSchedule()
    GetCommonNameItem = db.GetCommonNameItem(id)
    return render_template('UpdateFeeSchedule.html',title = GetCommonNameItem[0][0], ListFeeSchedule = ListFeeSchedule, GetCommonNameItem = GetCommonNameItem)

@app.route("/UpdateMatchFeeSchedule/<item_rn>/<id>", methods=['GET', 'POST'])
def UpdateMatchFeeSchedule(item_rn, id):
    db = Database()
    db.UpdateMatchFeeSchedule(item_rn, id)
    return redirect(url_for('ListMatchFeeSchedule'))

@app.route("/DeleteMatchFeeSchedule/<id>", methods=['GET', 'POST'])
def DeleteMatchFeeSchedule(id):
    db = Database()
    db.DeleteMatchFeeSchedule(id)
    return redirect(url_for('ListMatchFeeSchedule'))
