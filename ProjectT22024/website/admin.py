from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required,logout_user
from . import db
from .models import User, Influencer, Sponsor, Campaign,Request
from datetime import datetime

admin = Blueprint('admin',__name__)

#-------------------------------------------------------------------------------------------------#

#dashbaord
@admin.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
    if current_user.role == 'Admin':
        active_users = User.query.filter(User.role.in_(['Sponsor', 'Influencer'])).count()
        public_campaigns = Campaign.query.filter_by(visibility='public').count()
        private_campaigns = Campaign.query.filter_by(visibility='private').count()
        flagged_influencers = Influencer.query.filter_by(flagged=True).count()
        flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()

        stats = {
            'active_users': active_users,
            'public_campaigns': public_campaigns,
            'private_campaigns': private_campaigns,
            'flagged_influencers': flagged_influencers,
            'flagged_sponsors': flagged_sponsors,
        }

        return render_template('admin/stats.html', stats=stats)


#view influencers, campaigns or sponsors
@admin.route('/find', methods = ['GET','POST'])
@login_required
def view_entity():
    if current_user.role == 'Admin':
        if request.method == 'GET':
            entity="Campaign"
            item = Campaign.query.all()
            return render_template('admin/find.html', item=item, entity=entity)

        if request.method == 'POST':
            entity = request.form.get('entity')
            if entity == 'Influencer':
                item = Influencer.query.all()
            if entity == 'Campaign':
                item = Campaign.query.all()
            if entity == 'Sponsor':
                item = Sponsor.query.all()
            if entity == 'Request':
                item = Request.query.all()
        return render_template('admin/find.html', item=item, entity=entity)


#-------------------------------------------------------------------------------------------------#

#flag influencers, campaigns or sponsors
@admin.route('/flag_entity', methods = ['GET','POST'])
@login_required
def flag_entity():
    id = request.args.get('id')
    entity = request.args.get('entity')
    if current_user.role == 'Admin':
        if entity == 'Campaign':
            item = Campaign.query.get(id)
            if item:
                item.flagged = True
                db.session.commit()

        elif entity == 'Influencer':
            item = Influencer.query.get(id)
            if item:
                item.flagged = True
                db.session.commit()

        elif entity == 'Sponsor':
            item = Sponsor.query.get(id)
            if item:
                item.flagged = True 
                db.session.commit()
            db.session.commit()
        return redirect(url_for('admin.view_entity'))     
    return render_template('admin/find.html', item = item, entity = entity)


#-------------------------------------------------------------------------------------------------#

#unflag influencers, campaigns or sponsors
@admin.route('/unflag_entity', methods = ['GET','POST'])
@login_required
def unflag_entity():
    id = request.args.get('id')
    entity = request.args.get('entity')
    if current_user.role == 'Admin':
        if entity == 'Campaign':
            item = Campaign.query.get(id)
            if item:
                item.flagged = False

                db.session.commit()
        elif entity == 'Influencer':
            item = Influencer.query.get(id)
            if item:
                item.flagged = False
                db.session.commit()

        elif entity == 'Sponsor':
            item = Sponsor.query.get(id)
            if item:
                item.flagged = False 
                db.session.commit()
            return redirect(url_for('admin.view_entity'))  
        item=Campaign.query.all()
        return render_template('admin/find.html', item = item, entity = entity)

#-------------------------------------------------------------------------------------------------#

#remove influencers, campaigns or sponsors
@admin.route('/remove_entity', methods = ['GET','POST'])
@login_required
def remove_entity():
    id = request.args.get('id')
    entity = request.args.get('entity')
    if current_user.role == 'Admin':
        if entity == 'Campaign':
            item = Campaign.query.get(id)
            if item:
                db.session.delete(item)
        elif entity == 'Influencer':
            item = Influencer.query.get(id) 
            if item:
                db.session.delete(item)
        elif entity == 'Sponsor':
            item = Sponsor.query.get(id) 
            if item:
                db.session.delete(item)
        db.session.commit()
        return redirect(url_for('admin.view_entity'))   


#-------------------------------------------------------------------------------------------------#

#logout 
@admin.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user
    return redirect(url_for('auth.login'))
