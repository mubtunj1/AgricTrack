from flask import render_template, url_for, flash, redirect, request
from agrictrack.forms import RegistrationForm, LoginForm
from agrictrack import app, db, bcrypt
from agrictrack.models import User
from flask_login import login_user, current_user, logout_user, login_required



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
           next_page = request.args.get('next')
           return redirect(next_page) if next_page else redirect(url_for('home'))
        # if  form.email.data== 'admin@mubtunj.com' and form.password.data == 'password':
        #     
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')   
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/weatherupdate', methods=['GET', 'POST'])
def weather_report():
    if request.method == 'POST':
        city = request.form.get('city')
        api_key = 'cfeacba5d60826e68db04677b8ac9173'

        # Make a request to the weather API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Parse the required weather data from the API response
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']

            # Render the weather report template with the fetched data
            return render_template('weatherupdate.html', city=city, description=weather_description, temperature=temperature, humidity=humidity)
        else:
            error_message = data['message']
            return render_template('weatherupdate.html', error=error_message)

    return render_template('weatherupdate.html')