from flask import Blueprint, request, jsonify, redirect, url_for, abort
from models.tables import db, Review

bp = Blueprint("reviews", __name__, template_folder='templates')


@bp.route('/film/<int:film_id>/add_review', methods=['POST'])
def add_review(film_id):
    author = request.form['author']
    text = request.form['text']
    rating = request.form['rating']
    review = Review(author=author, text=text, rating=rating, film_id=film_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('film_card.api_film_detail', film_id=film_id))


@bp.route('/api/film/<int:film_id>/reviews')
def get_reviews(film_id):
    page = int(request.args.get('page', 1))
    per_page = 10
    reviews = Review.query.filter_by(film_id=film_id)\
        .order_by(Review.review_id.desc())\
        .paginate(page=page, per_page=per_page, error_out=False).items
    return jsonify([{
        "review_id": r.review_id,
        "author": r.author,
        "text": r.text,
        "rating": r.rating
    } for r in reviews])


@bp.route('/review/<int:review_id>/edit', methods=['POST'])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.author = request.form['author']
    review.text = request.form['text']
    review.rating = request.form['rating']
    db.session.commit()
    return jsonify({"success": True, "message": "Отзыв обновлён"})


@bp.route('/review/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({"success": True, "message": "Отзыв удалён"})
