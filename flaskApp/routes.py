from flask import render_template, url_for, flash, redirect, request, abort
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

@app.route("/highCost")
def highCost():
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # s = "select * from NHSO_OP_HIGH_COST"
    # cur.execute(s) # Execute the SQL
    # list_highcost = cur.fetchall()
    page = request.args.get('page', 1, type=int)
    student = Student.query.paginate(page= page, per_page= 15)
    # students = Student.query.all()
    return render_template('highcost.html',title='รายการ NHSO High Cost',student=student)

@app.route("/contactPlan")
def contactPlan():
    db = Database()
    list_plan = db.selectPlan()
    return render_template('contact_plan.html',title = 'จับคู่สิทธิ์การรักษา', list_plans = list_plan)