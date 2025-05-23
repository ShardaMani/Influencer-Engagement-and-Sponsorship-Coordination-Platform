from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



db=SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .admin import admin
    from .influencer import influencer
    from .sponsor import sponsor

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(influencer, url_prefix='/influencer')
    app.register_blueprint(sponsor, url_prefix='/sponsor')
    login_manager=LoginManager()
    login_manager.login_view="auth.login"
    login_manager.init_app(app)
    from .models import User, Influencer, Sponsor, Campaign, Request

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    create_database(app)
    
    return app

def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('database created !')

