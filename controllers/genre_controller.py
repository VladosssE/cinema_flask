from flask import Blueprint, request, render_template, redirect, url_for
from models.repo import GenreRepo
from models.tables import db, Genre
from flask_login import login_required

bp = Blueprint("genre", __name__, url_prefix="/genre")
repo = GenreRepo(db)

@bp.get("/")
@login_required
def list_genre():
    genre = repo.all()
    return render_template("list_genre.html", genre=genre)


@bp.post("/")
def create_genre():
    genre_name = reqeusrt.form.get("genre_name")
    budget = request.form.get("budget")
    budget_got = request.form.get("budget_got")
    country_prod = request.form.get("country_prod")
    language_orig = request.form.get("language_orig")
    director = request.form.get("director")
    repo.add(genre_name, budget, budget_got, country_prod, language_orig, director)
    return redirect(url_for("genre.list_genre"))


@bp.post("/<int:genre_id>/update")
def update_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    genre.genre_name = request.form.get("genre_name", genre.genre_name)
    genre.budget = request.form.get("budget", genre.budget)
    genre.budget_got = request.form.get("budget_got", genre.budget_got)
    genre.country_prod = request.form.get("country_prod", genre.country_prod)
    genre.language_orig = request.form.get("language_orig", genre.language_orig)
    genre.director = request.form.get("director", genre.director)
    db.session.commit()
    return redirect(url_for("genre.list_genre"))


@bp.post("/<int:genre_id>/delete")
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return redirect(url_for("genre.list_genre"))
