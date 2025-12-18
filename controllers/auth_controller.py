from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from models.user import UserRepo, User
bp = Blueprint("auth", __name__, url_prefix="/auth")

repo = UserRepo()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = repo.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash("Успешный вход!", "success")
            return redirect(url_for("index"))
        else:
            flash("Логин или пароль неверный", "error")
    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if repo.get_by_username(username):
            flash("Пользователь уже существует", "error")
        else:
            repo.add(username, password)
            flash("Успешно! Теперь авторизуйтесь.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")  

@bp.route("/logout")
@login_required
def logout():
    get_flashed_messages()
    logout_user()
    flash
    flash("Вы вышли.", "info")
    return redirect(url_for("auth.login"))

