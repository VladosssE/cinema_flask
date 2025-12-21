import pytest
import uuid
from sqlalchemy.exc import IntegrityError
from models.tables import Films, Genre, Review, db


def test_film_created(film):
    assert film.film_id is not None


def test_film_title(film):
    assert film.title == "Тестовый фильм"


def test_film_has_genre(film, genre):
    assert genre in film.genres


def test_genre_unique_constraint(app):
    name = f"Комедия-{uuid.uuid4()}"

    g1 = Genre(genre_name=name)
    db.session.add(g1)
    db.session.commit()

    g2 = Genre(genre_name=name)
    db.session.add(g2)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_review_relation(app, film):
    review = Review(author="Ivan", text="Отлично", rating=9, film=film)
    db.session.add(review)
    db.session.commit()
    assert review in film.reviews


def test_film_repr(film):
    assert "Films" in repr(film)


def test_genre_repr(genre):
    assert "Genre" in repr(genre)
