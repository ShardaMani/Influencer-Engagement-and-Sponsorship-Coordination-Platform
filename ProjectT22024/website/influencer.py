from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from .models import User,Influencer, Request,Campaign, Sponsor
from . import db
influencer = Blueprint('influencer',__name__)

#-------------------------------------------------------------------------------------------------#

#influencer dashboard
@influencer.route('/influencer/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if current_user.role == 'Influencer':
        if request.method == 'GET':
            influencer = Influencer.query.filter_by(user_id=current_user.user_id).first()
            return render_template('influencer/dashboard.html', influencer=influencer)

#-------------------------------------------------------------------------------------------------#
#influencer profile  
@influencer.route('/influencer/profile', methods=['GET','POST'])
@login_required
def profile():
    if current_user.role == 'Influencer':
        if request.method=="GET":
            user = User.query.filter_by(user_id=current_user.user_id).first()
            influencer_detail = Influencer.query.filter_by(user_id=current_user.user_id).first()
            return render_template('influencer/profile.html',user=user,influencer=influencer_detail)
        
        
        if request.method == 'POST':
            user = User.query.filter_by(user_id=current_user.user_id).first()
            influencer_detail = Influencer.query.filter_by(user_id=current_user.user_id).first()
            if influencer_detail:
                user.name = request.form.get('name')
                influencer_detail.gender = request.form.get('gender')
                if request.form.get('password'):
                    influencer_detail.password = request.form.get('password')

                influencer_detail.contact = request.form.get('contact')
                influencer_detail.name = request.form.get('name')

                influencer_detail.category = request.form.get('category')
                influencer_detail.niche = request.form.get('niche')
                influencer_detail.platform_presence = request.form.get('platform_presence')
                influencer_detail.followers = request.form.get('followers')
                db.session.commit()
                return redirect(url_for('influencer.dashboard'))

            else:
                if request.form.get('password'):
                    user.password = request.form.get('password')
                influencer = Influencer(
                        user_id = current_user.user_id, name = request.form.get('name'), gender = request.form.get('gender'),category = request.form.get('category'),niche = request.form.get('niche'),followers = request.form.get('followers'),contact = request.form.get('contact'),platform_presence = request.form.get('platform_presence')
                    )
                db.session.add(influencer)
                db.session.commit()
                return redirect(url_for('influencer.dashboard'))

            return render_template('influencer/profile.html',user=user,influencer=influencer_detail)
    
#-------------------------------------------------------------------------------------------------#

#view_requests
@influencer.route('/influencer', methods=['GET','POST'])
@login_required
def view_requests():
    if current_user.role == 'Influencer':
        if request.method == 'GET':
            received_requests = Request.query.filter_by(influencer_id=current_user.user_id, sent_by_sponsor=True).all()
            sent_requests = Request.query.filter_by(influencer_id=current_user.user_id, sent_by_influencer=True).all()
            return render_template('influencer/request/view_request.html', received_requests=received_requests, sent_requests=sent_requests)

#-------------------------------------------------------------------------------------------------#

#accept_requests
@influencer.route('/influencer/accept/<int:id>', methods=['GET','POST'])
@login_required
def handle_new_requests(id):
    if current_user.role == 'Influencer':
        requested = Request.query.get(id)
        action = request.form.get('action')
        if action == 'accept':
            requested.status = 'Accepted'
        elif action == 'reject':
            requested.status = 'Rejected'
        db.session.commit()
        return redirect(url_for('influencer.view_requests'))
        

#-------------------------------------------------------------------------------------------------#

#negogtiating payment
@influencer.route('/influencer/negotiate/<int:id>', methods=['GET','POST'])
@login_required
def negotiate(id):
    if current_user.role == 'Influencer':
        if request.method == 'GET':
            requested = Request.query.get(id)
            return render_template('Influencer/request/negotiate.html', requested=requested)
        if request.method == 'POST':
            requested = Request.query.get(id)
            negotiated_payment = request.form.get('negotiate')
            requested.status = 'negotiating'
            db.session.commit()
            return redirect(url_for('influencer.view_requests'))
        
#-------------------------------------------------------------------------------------------------#
#search for campaigns
@influencer.route('/search_campaigns', methods=['GET', 'POST'])
def search_campaigns():
    if current_user.role == 'Influencer':
        campaigns = []
        if request.method == 'POST':
            search =request.form.get('search')
            campaigns = Campaign.query.filter_by(visibility='public')
            campaigns = Campaign.query.filter(Campaign.name == search).all() + Campaign.query.filter(Campaign.description.like('%' + search + '%')).all()
            if campaigns:
                return render_template('influencer/search_campaigns.html', campaigns=campaigns)
            else:
                return render_template('influencer/search_campaigns.html', message = 'no campaigns found')
        return render_template('influencer/search_campaigns.html')

#-------------------------------------------------------------------------------------------------#

#send request
@influencer.route('/search_campaigns/send_request', methods=['GET', 'POST'])
@login_required
def send_request():
    if current_user.role == 'Influencer':
        if request.method == 'GET':
            return render_template('influencer/request/create_request.html')
        if request.method == 'POST':
            sponsor_id = request.form.get('sponsor_id')
            campaign_id = request.form.get('campaign_id')
            campaign_name = request.form.get('campaign_name')
            message = request.form.get('message')
            requirements = request.form.get('requirements')
            payment_amount = request.form.get('payment_amount')
            new_request = Request(message = message, requirements = requirements, payment = payment_amount, status='pending', influencer_id=current_user.user_id, sponsor_id = sponsor_id, campaign_id=campaign_id,
                sent_by_influencer=True)
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('influencer.view_requests'))
        return render_template('influencer/request/create_request.html')
#-------------------------------------------------------------------------------------------------#

#logout 
@influencer.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user
    return redirect(url_for('auth.login'))


