from flask import Flask, render_template
from models.tables import db, Films
from controllers.auth_controller import bp as auth_bp
from controllers.genre_controller import bp as genre_bp
from controllers.film_card_controller import bp as film_card_bp
from controllers.review_controller import bp as review_bp
from flask_login import LoginManager
from models.user import User
import pymysql

def create_app(test_config=None):
    connection = pymysql.connect( host='localhost', user='root', password='root' )
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS cinema_db;")
            cursor.execute("CREATE USER IF NOT EXISTS 'filmuser'@'%' IDENTIFIED BY 'filmfilm';")
            cursor.execute("GRANT REFERENCES, SELECT, CREATE, INSERT, UPDATE, DELETE ON cinema_db.* TO 'filmuser'@'%';")
            cursor.execute("FLUSH PRIVILEGES;")
            connection.commit()
    finally:
        connection.close()
    app = Flask(__name__, template_folder="views", static_folder="static")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://filmuser:filmfilm@localhost/cinema_db'
    app.config['SECRET_KEY'] = '000'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(genre_bp)
    app.register_blueprint(film_card_bp)
    app.register_blueprint(review_bp)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Войдите в систему'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        films = Films.query.all()
        return render_template('index.html', films=films)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
