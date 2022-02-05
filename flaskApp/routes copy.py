from flask import render_template, url_for, flash, redirect, request, abort
from flaskApp.forms import  LoginForm
from flaskApp import app, db
from flaskApp.models import Student
# import psycopg2
# import psycopg2.extras


# DB_HOST = "localhost"
# DB_NAME = "imed_db"
# DB_USER = "postgres"
# DB_PASS = 'postgres'


# conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST )



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