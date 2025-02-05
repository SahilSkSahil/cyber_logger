from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create an instance of SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Define the User model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(150), nullable=False)  # User's password (hashed)

    def __repr__(self):
        return f'<User  {self.username}>'

# Define the Incident model (table)
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each incident
    title = db.Column(db.String(100), nullable=False)  # Title of the incident
    description = db.Column(db.Text, nullable=False)  # Description of the incident
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Time when the incident was reported
    status = db.Column(db.String(50), default='Open')  # Status of the incident (e.g., 'Open', 'Resolved')
    resolution_notes = db.Column(db.Text, nullable=True)  # Notes related to the resolution of the incident

    def __repr__(self):
        return f'<Incident {self.id} - {self.title} - {self.status}>'