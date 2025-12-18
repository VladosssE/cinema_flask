from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

film_genre = db.Table(
    'film_genre',
    db.Column('film_id', db.Integer, db.ForeignKey('films.film_id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
)

class Films(db.Model):
    __tablename__ = 'films'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125), nullable=False)
    orig_title = db.Column(db.String(125))
    descr = db.Column(db.Text)
    release_year = db.Column(db.Date)
    duration = db.Column(db.Integer)
    age_rate = db.Column(db.String(3))
    rating = db.Column(db.Numeric(3,1), server_default=text("'0.0'"))
    image_url = db.Column(db.String(80), server_default=text("'no_film.jpg'"))
    genres = db.relationship("Genre", secondary=film_genre, backref="films")

    def __repr__(self):
        return f'<Films {self.title}>'


class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(125), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.genre_name}>'


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(125))
    text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    film_id = db.Column(db.Integer, db.ForeignKey('films.film_id'))
    film = db.relationship("Films", backref="reviews")

    def __repr__(self):
        return f'<Review {self.author}>'
