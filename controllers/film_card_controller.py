from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from models.repo import FilmsRepo
from models.tables import db, Films, Genre
from flask_login import login_required
import os
from sqlalchemy import or_

bp = Blueprint("film_card", __name__, template_folder='templates')
repo = FilmsRepo(db)

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

    return render_template(
        "index.html",
        films=films,
        posters_img=sorted(posters_img),
        all_genres=all_genres
    )

@bp.route("/api/film/add", methods=["POST"])
@login_required
def api_add_film():
    data = request.json
    genres_ids = data.get('genres', [])
    new_film = repo.add(
        title=data.get('title'),
        orig_title=data.get('orig_title'),
        descr=data.get('descr'),
        release_year=data.get('release_year'),
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


@bp.route("/api/film/<int:film_id>/edit", methods=["POST"])
@login_required
def api_edit_film(film_id):
    film = Films.query.get_or_404(film_id)
    data = request.json

    film.title = data.get('title', film.title)
    film.orig_title = data.get('orig_title', film.orig_title)
    film.descr = data.get('descr', film.descr)
    film.release_year = data.get('release_year', film.release_year)
    film.duration = data.get('duration', film.duration)
    film.age_rate = data.get('age_rate', film.age_rate)
    film.image_url = data.get('image_url', film.image_url)
    genre_ids = data.get('genres', [])
    
    film.genres = Genre.query.filter(Genre.genre_id.in_(genre_ids)).all()

    db.session.commit()
    return jsonify({"success": True})


@bp.route('/film/<int:film_id>/delete', methods=['POST'])
@login_required
def delete_film(film_id):
    film = Films.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return redirect(url_for('film_card.list_film'))


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
