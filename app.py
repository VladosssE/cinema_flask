from flask import Flask, render_template
from models.tables import db, Films, Genre
from controllers.auth_controller import bp as auth_bp
from controllers.genre_controller import bp as genre_bp
from controllers.film_card_controller import bp as film_card_bp
from controllers.review_controller import bp as review_bp
from flask_login import LoginManager
from models.user import User

def create_app(test_config=None):
    app = Flask(__name__, template_folder="views", static_folder="static")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema_db.sqlite'
    app.config['SECRET_KEY'] = '000'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

        if not Genre.query.first():
            genres = [
                (1, 'Боевик'), (2, 'Комедия'), (3, 'Драма'), (4, 'Фантастика'), 
                (5, 'Ужасы'), (6, 'Триллер'), (7, 'Приключения'), (8, 'Мультфильм'),
                (9, 'Анимация'), (10, 'Мюзикл'), (11, 'Романтика'), (12, 'Документальный'),
                (13, 'Исторический'), (14, 'Фэнтези'), (15, 'Семейный'), (16, 'Криминал'),
                (17, 'Военный'), (18, 'Спорт'), (19, 'Музыкальный'), (20, 'Мелодрама'),
                (21, 'Западный'), (22, 'Детектив'), (23, 'Психологический'), (24, 'Эпический'),
                (25, 'Политический'), (26, 'Постапокалипсис'), (27, 'Киберпанк'), (28, 'Детский'),
                (29, 'Антиутопия'), (30, 'Мистика'), (31, 'Классика'), (32, 'Экшн-комедия'),
                (33, 'Трагикомедия'), (34, 'Сенсационный'), (35, 'Сатирический'), (36, 'Реализм'),
                (37, 'Нуар'), (38, 'Артхаус'), (39, 'Биография'), (40, 'Семейная комедия'),
                (41, 'Технотриллер'), (42, 'Приключенческая комедия'), (43, 'Молодежный'),
                (44, 'Философский'), (45, 'Пародия'), (46, 'Историческая драма'), (47, 'Докудрама'),
                (48, 'Короткометражка'), (49, 'Литературная экранизация'), (50, 'Сказка'),
                (51, 'Супергеройский'), (52, 'Катастрофа'), (53, 'Выживание'), (54, 'Путешествия во времени'),
                (55, 'Космическая опера'), (56, 'Псевдодокументальный'), (57, 'Мокьюментари'), (58, 'Роуд-муви'),
                (59, 'Хоррор-комедия'), (60, 'Романтическая комедия'), (61, 'Юридическая драма'),
                (62, 'Медицинская драма'), (63, 'Шпионский'), (64, 'Гангстерский'), (65, 'Психологический триллер'),
                (66, 'Социальная драма'), (67, 'Экспериментальный'), (68, 'Фильм-катастрофа'), (69, 'Мифология'),
                (70, 'Экранизация комикса'), (71, 'Нео-нуар'), (72, 'Космический триллер'), (73, 'Романтическая драма'),
                (74, 'Криминальная комедия'), (75, 'Фантастический триллер')
            ]
            for gid, gname in genres:
                db.session.add(Genre(genre_id=gid, genre_name=gname))
            db.session.commit()

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
