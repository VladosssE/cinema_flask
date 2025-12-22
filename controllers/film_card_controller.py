from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from models.repo import FilmsRepo
from models.tables import db, Films, Genre, Review
from flask_login import login_required
import os
from sqlalchemy import or_, func
from datetime import datetime


bp = Blueprint("film_card", __name__, template_folder='templates')
repo = FilmsRepo(db)


#Форматирование даты (Чтобы работала переменная db.Date())
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


#Вывод фильмов из базы данных на страницу и функция поиска
@bp.get("/")
def list_film():
    search = request.args.get("q", "").strip()
    query = Films.query
    if search:
        query = query.filter(
            or_(
                Films.title.ilike(f"%{search}%"),
                Films.orig_title.ilike(f"%{search}%")
            )
        )

    films = query.all()
    all_genres = Genre.query.all()

    images_dir = os.path.join(current_app.root_path, "static", "images")
    posters_img = [
        f for f in os.listdir(images_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        and f.lower() not in ("placeholder.jpg", "no_film.jpg")
    ]

    return render_template("index.html", films=films, posters_img=sorted(posters_img), all_genres=all_genres)


#Добавление фильма
@bp.route("/api/film/add", methods=["POST"])
@login_required
def api_add_film():
    data = request.json
    genres_ids = data.get('genres', [])
    release_year = parse_date(data.get('release_year'))

    new_film = repo.add(
        title=data.get('title'),
        orig_title=data.get('orig_title'),
        descr=data.get('descr'),
        release_year=release_year,
        duration=data.get('duration'),
        age_rate=data.get('age_rate'),
        rating=0.0,
        image_url=data.get('image_url')
    )

    if genres_ids:
        genres = Genre.query.filter(Genre.genre_id.in_(genres_ids)).all()
        new_film.genres = genres
        db.session.commit()

    return jsonify({"success": True, "film_id": new_film.film_id})


#Изменение фильма
@bp.route("/api/film/<int:film_id>/edit", methods=["POST"])
@login_required
def api_edit_film(film_id):
    film = Films.query.get_or_404(film_id)
    data = request.json

    film.title = data.get('title', film.title)
    film.orig_title = data.get('orig_title', film.orig_title)
    film.descr = data.get('descr', film.descr)
    release_year_str = data.get('release_year')
    if release_year_str is not None:
        film.release_year = parse_date(release_year_str)
    film.duration = data.get('duration', film.duration)
    film.age_rate = data.get('age_rate', film.age_rate)
    film.image_url = data.get('image_url', film.image_url)

    genre_ids = data.get('genres', [])
    if genre_ids:
        film.genres = Genre.query.filter(Genre.genre_id.in_(genre_ids)).all()

    db.session.commit()
    return jsonify({"success": True})


#Удаление фильма
@bp.route('/film/<int:film_id>/delete', methods=['POST'])
@login_required
def delete_film(film_id):
    film = Films.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return redirect(url_for('film_card.list_film'))


#Подробности фильма в модальном окне
@bp.route('/api/film/<int:film_id>')
def api_film_detail(film_id):
    film = Films.query.get_or_404(film_id)
    return jsonify({
        "film_id": film.film_id,
        "title": film.title,
        "orig_title": film.orig_title,
        "descr": film.descr,
        "release_year": film.release_year.strftime('%Y-%m-%d') if film.release_year else "",
        "duration": film.duration,
        "age_rate": film.age_rate,
        "rating": str(film.rating),
        "image_url": film.image_url,
        "genres": [
            {
                "genre_id": g.genre_id,
                "genre_name": g.genre_name
            } for g in film.genres
        ],
        "reviews": [{"author": r.author, "text": r.text} for r in film.reviews]
    })


#Статистика
@bp.route('/stats')
def statistics():
    ALL_AGES = ['0+', '6+', '12+', '16+', '18+']
    total_films = db.session.query(func.count(Films.film_id)).scalar()
    films_by_age_raw = (
        db.session.query(Films.age_rate, func.count(Films.film_id))
        .group_by(Films.age_rate)
        .all()
    )
    films_by_age_dict = {
        age: count for age, count in films_by_age_raw
    }
    films_by_age = [
        (age, films_by_age_dict.get(age, 0))
        for age in ALL_AGES
    ]

    films_by_genre = (
        db.session.query(Genre.genre_name, func.count(Films.film_id))
        .join(Genre.films)
        .group_by(Genre.genre_name)
        .all()
    )

    avg_rating = db.session.query(func.avg(Films.rating)).scalar()
    total_reviews = db.session.query(func.count(Review.review_id)).scalar()

    return render_template(
        'statistics.html',
        total_films=total_films,
        films_by_age=films_by_age,
        films_by_genre=films_by_genre,
        avg_rating=round(avg_rating or 0, 1),
        total_reviews=total_reviews
    )
