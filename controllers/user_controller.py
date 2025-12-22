from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import UserRepo, User, db

bp = Blueprint("user", __name__, url_prefix="/users")
repo = UserRepo()

@bp.route('/', methods=['GET', 'POST'])
@login_required
def list_users():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            username = request.form.get("username")
            password = request.form.get("password")
            if repo.get_by_username(username):
                flash("Пользователь уже существует", "error")
            else:
                repo.add(username, password)
                flash("Пользователь добавлен", "success")

        else:
            user_id = int(request.form.get("user_id"))
            user = User.query.get_or_404(user_id)

            if action == "update":
                new_username = request.form.get("username")
                existing_user = User.query.filter(User.username == new_username, User.id != user_id).first()
                if existing_user:
                    flash("Пользователь уже существует", "error")
                else:
                    user.username = new_username
                    db.session.commit()
                    flash("Пользователь изменен", "success")

            elif action == "delete":
                if user.id == current_user.id:
                    flash("Удаление самого себя (Ну нельзя)", "error")
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash("Пользователь удалён", "info")

        return redirect(url_for("user.list_users"))

    users = User.query.all()
    return render_template("users/list_users.html", users=users)


@bp.route('/add', methods=['POST'])
@login_required
def add_user():
    username = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter_by(username=username).first():
        flash("Логин уже занят", "error")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Пользователь добавлен", "success")

    return redirect(url_for("user.list_users"))
