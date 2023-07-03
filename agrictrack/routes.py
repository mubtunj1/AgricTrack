from flask import render_template, url_for, flash, redirect, request
from agrictrack.forms import RegistrationForm, LoginForm
from agrictrack import app, db, bcrypt
from agrictrack.models import User
from flask_login import login_user, current_user, logout_user



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # add the user to the database
        db.session.commit() # commit the changes
        flash(f'Account created for {form.username.data}!','success')   
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember.data)
           #next_page = request.args.get('next')
           return redirect(url_for('home'))
        # if  form.email.data== 'admin@mubtunj.com' and form.password.data == 'password':
        #     
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')   
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))