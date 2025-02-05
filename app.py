from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, Incident, User  # Import User model and db instance
from forms import IncidentForm, UserForm, LoginForm  # Import forms
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Change this to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress a warning

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')  # Render the index template

@app.route('/report', methods=['GET', 'POST'])
@login_required  # Protect this route
def report_incident():
    form = IncidentForm()
    if form.validate_on_submit():
        # Create a new incident
        new_incident = Incident(
            title=form.title.data,
            description=form.description.data,
            status='Open',  # Default status
            resolution_notes=form.resolution_notes.data
        )
        db.session.add(new_incident)
        db.session.commit()
        flash('Incident reported successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('report_incident.html', form=form)

@app.route('/dashboard')
@login_required  # Protect this route
def dashboard():
    incidents = Incident.query.all()
    return render_template('dashboard.html', incidents=incidents)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        try:
            # Hash the password before storing it
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User  registered successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash('An error occurred while registering. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required  # Protect this route
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)