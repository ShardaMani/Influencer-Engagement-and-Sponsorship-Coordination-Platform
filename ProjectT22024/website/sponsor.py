from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime
from .models import User, Campaign, Influencer, Sponsor,Request
from . import db


sponsor = Blueprint('sponsor',__name__)

#-------------------------------------------------------------------------------------------------#
#sponsor dashboard
@sponsor.route('/dashboard', methods =['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            return render_template('sponsor/dashboard.html')

#-------------------------------------------------------------------------------------------------#
#sponsor profile
@sponsor.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            sponsor_detail = Sponsor.query.filter_by(user_id=current_user.user_id).first()
            return render_template('sponsor/show_profile.html', sponsor = sponsor_detail) 
        
        if request.method == 'POST':
            return redirect(url_for('sponsor.edit_profile'))


#---------------------------------------------------------------------------------------------------#
#not working
#edit profile
@sponsor.route('/edit_profile', methods =['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            user = User.query.filter_by(user_id=current_user.user_id).first()
            sponsor_detail = Sponsor.query.filter_by(user_id=current_user.user_id).first()
            return render_template('Sponsor/edit_profile.html',user=user,sponsor = sponsor_detail)


        if request.method == 'POST':
            sponsor_detail = Sponsor.query.filter_by(user_id=current_user.user_id).first()
            if sponsor_detail:
                sponsor_detail.company_name = request.form.get('company_name')
                sponsor_detail.industry = request.form.get('industry')
                sponsor_detail.budget = request.form.get('budget')

                db.session.commit()
                return redirect(url_for('sponsor.profile'))

            else:
                company_name = request.form.get('name')
                industry = request.form.get('industry')
                budget = request.form.get('budget')
                flagged = False

                sponsor = Sponsor(company_name = company_name, industry = industry, budget = budget, flagged = flagged, user_id = current_user.user_id)
                db.session.add(sponsor)
                db.session.commit()
                return redirect(url_for('sponsor.profile'))
            
            return render_template('sponsor.edit_profile.html', sponsor=sponsor_detail)


#---------------------------------------------------------------------------------------------------#

#view_campaigns:
@sponsor.route('/campaign', methods=['GET','POST'])
@login_required
def view_campaign():
    if current_user.role == 'Sponsor':
        campaigns = Campaign.query.filter_by(sponsor_id=current_user.user_id).all()
        if campaigns:
            return render_template('sponsor/campaigns/view_campaign.html',campaigns=campaigns)
        
        return render_template('sponsor/campaigns/view_campaign.html')
#-------------------------------------------------------------------------------------------------#

#add campaign
@sponsor.route('/campaign/add', methods=['GET','POST'])
@login_required
def add_campaign():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            return render_template('sponsor/campaigns/add_campaign.html')

        if request.method == 'POST':
            id = current_user.user_id
            campaign_name = request.form.get('name')
            visibility = request.form.get('visibility')
            desc = request.form.get('description')
            start = request.form.get('start_date','%Y-%m-%d')
            start= datetime.strptime(start, '%Y-%m-%d')
            end = request.form.get('end_date','%Y-%m-%d')
            end= datetime.strptime(end, '%Y-%m-%d')
            budget = request.form.get('budget')
            goals = request.form.get('goals')

            #adding data in Campaign
            campaign = Campaign(name = campaign_name, visibility = visibility, description = desc, start_date = start, end_date = end, budget= budget, goals = goals, sponsor_id = id)
            db.session.add(campaign)
            db.session.commit()

            return redirect(url_for('sponsor.view_campaign'))

#-------------------------------------------------------------------------------------------------#

#edit campaign details
@sponsor.route('/campaign/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_campaign(id):
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            campaign = Campaign.query.get(id)
            return render_template('sponsor/campaigns/edit_campaign.html',campaign=campaign)

        if request.method == 'POST':
            campaign_name = request.form.get('name')
            visibility = request.form.get('visibility')
            desc = request.form.get('description')
            start = request.form.get('start_date','%Y-%m-%d')
            start= datetime.strptime(start, '%Y-%m-%d')
            end = request.form.get('end_date','%Y-%m-%d')
            end= datetime.strptime(end, '%Y-%m-%d')
            budget = request.form.get('budget')
            goals = request.form.get('goals')

            campaign = Campaign.query.get(id)
            campaign.name=campaign_name
            campaign.visibility=visibility
            campaign.description=desc
            campaign.start_date=start
            campaign.end_date=end
            campaign.budget=budget
            campaign.goals=goals

            db.session.commit()

            return redirect(url_for('sponsor.view_campaign'))

#-------------------------------------------------------------------------------------------------#

#delete campaign
@sponsor.route('/campaign/delete/<int:id>', methods = ['GET','POST'])
@login_required
def delete_campaign(id):
    if current_user.role == 'Sponsor':
        campaign = Campaign.query.get(id)
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for('sponsor.view_campaign'))

#-------------------------------------------------------------------------------------------------#

#request

#view ad
@sponsor.route('/request')
@login_required
def view_requests():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            received_requests = Request.query.filter_by(sponsor_id=current_user.user_id, sent_by_influencer=True).all()
            sent_requests = Request.query.filter_by(sponsor_id=current_user.user_id, sent_by_sponsor=True).all()
            return render_template('sponsor/ad request/view_ad.html', received_requests=received_requests, sent_requests=sent_requests)

#-------------------------------------------------------------------------------------------------#

#create ad
@sponsor.route('/request/add', methods=['GET','POST'])
@login_required
def add_requests():
    if current_user.role == 'Sponsor':
        if request.method == 'GET':
            return render_template('sponsor/ad request/create_ad.html')
        if request.method == 'POST':
            influencer_id = request.form.get('influencer_id')
            campaign_id = request.form.get('campaign_id')
            message = request.form.get('message')
            requirements=request.form.get('requirements')
            payment = request.form.get('payment')
            status = 'pending'

            requests = Request(campaign_id = campaign_id, message = message, requirements = requirements, payment = payment, status = status, influencer_id = influencer_id, sponsor_id=current_user.user_id,
                sent_by_sponsor=True)
            db.session.add(requests)
            db.session.commit()
            return redirect(url_for('sponsor.view_requests'))
        return render_template('sponsor/ad request/create_ad.html')


#---------------------------------------------------------------------------------------------------#

#edit request
@sponsor.route('/request/edit/<int:id>',methods=['GET','POST']) 
@login_required
def edit_requests(id):
    if current_user.role == 'Sponsor':
        if request.method == 'POST':
            message = request.form.get('message')
            requirements=request.form.get('requirements')
            payment = request.form.get('payment')

            requests = Request.query.all(id)
            requests.message = request.form.get('message')
            requests.requirements=request.form.get('requirements')
            requests.payment = request.form.get('payment')
            
            db.session.commit()

            return redirect(url_for('sponsor.view_requests'))
        return render_template('sponsor/ad request/edit_ad.html')

#---------------------------------------------------------------------------------------------------#

#delete request
@sponsor.route('/request/delete/<int:id>', methods = ['GET','POST'])
@login_required
def delete_requests(id):
    if current_user.role == 'Sponsor':
        requests = Request.query.get(id)
        db.session.delete(requests)
        db.session.commit()
        return redirect(url_for('sponsor.view_requests'))


#---------------------------------------------------------------------------------------------------#

#handle new requests
@sponsor.route('/request/handle_new_requests/<int:id>', methods = ['GET', 'POST'])
@login_required
def handle_new_requests(id):
    if current_user.role == 'Sponsor':
        if request.method == 'POST':
            action = request.form.get('action')
            recieved_requests = Request.query.get(id)
            if action == 'accept':
                recieved_requests.status = 'accepted'
            elif action == 'reject':
                recieved_requests.status = 'rejected'
            db.session.commit()
            return redirect(url_for('sponsor.view_requests'))

#---------------------------------------------------------------------------------------------------#

#search influencer
@sponsor.route('/search_influencer', methods = ['GET','POST'])
@login_required
def search_influencer():
    if current_user.role == 'Sponsor':
        influencers = []
        if request.method == 'POST':
            niche = request.form.get('niche')
            min_followers = request.form.get('min_followers')
            
            query = Influencer.query
            if niche:
                query = query.filter(Influencer.niche == niche)
            if min_followers:
                query = query.filter(Influencer.followers >= int(min_followers))
            
            influencers = query.all()
            
        return render_template('sponsor/search_influencer.html', influencers=influencers)



#-------------------------------------------------------------------------------------------------#

#logout

@sponsor.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user
    return redirect(url_for('auth.login'))





