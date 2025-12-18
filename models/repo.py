from models.tables import db, Films, Genre

class FilmsRepo:
    def __init__(self, db_instance=None):
        if db_instance:
            global db
            db = db_instance

    def all(self):
        return Films.query.all()

    def add(self, title, orig_title, descr, release_year, duration, age_rate, rating, image_url):
        new_film = Films(
            title=title,
            orig_title=orig_title,
            descr=descr,
            release_year=release_year,
            duration=duration,
            age_rate=age_rate,
            rating=rating,
            image_url=image_url if image_url else None
            )
        db.session.add(new_film)
        db.session.commit()
        return new_film

class GenreRepo:
    def __init__(self, db_instance=None):
        if db_instance:
            global db
            db = db_instance

    def all(self):
        return Genre.query.all()

    def add(self, genre_name, budget, budget_got, country_prod, language_orig, director):
        new_genre = Genre(
            genre_name=genre_name,
            budget=budget,
            budget_got=budget_got,
            country_prod=country_prod,
            language_orig=language_orig,
            director=director
            )
        db.session.add(new_genre)
        db.session.commit()
        return new_genre
