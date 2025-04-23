from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    influencer = db.relationship('Influencer', uselist=False, backref='user')
    sponsor = db.relationship('Sponsor', uselist=False, backref='user')

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def get_id(self):
        return (self.user_id)



class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = True)
    gender = db.Column(db.String(20), nullable = True)
    contact = db.Column(db.String(10), nullable = True)
    category = db.Column(db.String(150), nullable=True)
    niche = db.Column(db.String(150), nullable=True)
    platform_presence = db.Column(db.String(150), nullable=True)
    followers = db.Column(db.Integer, nullable = True)
    flagged = db.Column(db.Boolean, default=False)
    
    requests = db.relationship('Request', backref='influencer')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), unique=True, nullable=True)
    industry = db.Column(db.String(150), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    flagged = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    campaigns = db.relationship('Campaign', backref='sponsor')
    requests = db.relationship('Request', backref='sponsor')

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(50), default='private')
    goals = db.Column(db.String(100), nullable=False)
    flagged = db.Column(db.Boolean, default=False)

    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    requests = db.relationship('Request', backref='campaign')

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    sent_by_influencer = db.Column(db.Boolean, default=False)
    sent_by_sponsor = db.Column(db.Boolean, default=False)

    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    
    