from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from .models import User, Sponsor, Influencer
from . import db

auth = Blueprint('auth',__name__)

#-------------------------------------------------------------------------------------------------#
#login user
@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        user = User.query.filter_by(email = email).first()
        if not user:
            return redirect(url_for('auth.login', message = 'user does not exit. Sign-up required'))

        if user.password != password:
            return redirect(url_for('auth.login', message='wrong password. Retry!'))
  
        if user.role == 'Admin':
            login_user(user)
            return redirect(url_for('admin.dashboard', message= 'Login successful'))

        elif user.role == 'Influencer':
            
            
            login_user(user)
            return redirect(url_for('influencer.dashboard',  message= 'Login successful'))
        
        elif user.role == 'Sponsor':
            
            
            login_user(user)
            return redirect(url_for('sponsor.view_campaign',  message= 'Login successful', type ='success'))
    return render_template("login.html")
        

#-------------------------------------------------------------------------------------------------#

#Register new user 
@auth.route('/register', methods = ['GET','POST'])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method == 'POST':
        name=request.form.get('Name')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        role = request.form.get('role')
        user = User.query.filter_by(email = email).first()
        if user:
            return redirect(url_for('auth.login', message = 'user already exists. Login to continue'))
        if password1 != password2:
            return redirect(url_for('auth.register', message = 'passwords do not match'))
        new_user = User(email=email, name=name, password=password1, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login', message = 'registered succesfully. login to continue', type = 'success'))

#-------------------------------------------------------------------------------------------------#
#logout user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
      



