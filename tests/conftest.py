import pytest
import sys
import os
import uuid
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from app import create_app
from models.tables import db, Films, Genre


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def genre(app):
    g = Genre(genre_name=f"Драма-{uuid.uuid4()}")
    db.session.add(g)
    db.session.commit()
    return g


@pytest.fixture
def film(app, genre):
    f = Films(
        title="Тестовый фильм",
        orig_title="Test Movie",
        descr="Описание фильма",
        release_year=date(2020, 1, 1),
        duration=120,
        age_rate="16+",
        image_url="test.jpg"
    )
    f.genres.append(genre)
    db.session.add(f)
    db.session.commit()
    return f
