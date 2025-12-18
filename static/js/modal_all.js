document.addEventListener('DOMContentLoaded', () => {
	const modal = document.getElementById("filmInfo");
	const closeButtons = modal ? modal.getElementsByClassName("close") : [];
	const modals = document.querySelectorAll('.modal');

	let currentReviewPage = 1;
	let loadingReviews = false;
	let currentFilmId = null;

	async function loadReviews(filmId, page = 1) {
		const reviewsList = document.getElementById('filmReviews');
		if (!reviewsList) return;

		try {
			const response = await fetch(`/api/film/${filmId}/reviews?page=${page}`);
			if (!response.ok) return;

			const reviews = await response.json();

			if (reviews.length === 0 && page === 1) {
				reviewsList.innerHTML = '<li>Пока нет отзывов.</li>';
				return;
			}

			if (page === 1) reviewsList.innerHTML = '';

			reviews.forEach(r => {
				const li = document.createElement('li');
				li.classList.add('review-item');
				li.dataset.reviewId = r.review_id;

				const textSpan = document.createElement('span');
				textSpan.className = 'review-text';
				textSpan.innerHTML = `<strong>${r.author}:</strong> ${r.text}`;

				const ratingSpan = document.createElement('span');
				ratingSpan.className = 'review-rating';
				ratingSpan.innerText = `${r.rating}/10`;

				li.appendChild(textSpan);
				li.appendChild(ratingSpan);

				if (IS_AUTHENTICATED === true || IS_AUTHENTICATED === 'true') {
					const editBtn = document.createElement('button');
					editBtn.className = 'edit-review';
					editBtn.innerText = 'Изменить';

					const deleteBtn = document.createElement('button');
					deleteBtn.className = 'delete-review';
					deleteBtn.innerText = 'Удалить';

					li.appendChild(editBtn);
					li.appendChild(deleteBtn);
				}

				reviewsList.appendChild(li);
			});

			attachReviewButtons(filmId);

		} catch (err) {
			console.error('Ошибка загрузки отзывов:', err);
		}
	}

	function attachReviewButtons(filmId) {
		const reviewsList = document.getElementById('filmReviews');

		reviewsList.querySelectorAll('.edit-review').forEach(btn => {
			btn.onclick = async (e) => {
				e.stopPropagation();
				const li = btn.closest('li');
				const reviewId = li.dataset.reviewId;

				const currentAuthor = li.querySelector('.review-text strong').innerText.replace(':', '');
				const currentText = li.querySelector('.review-text').innerText.replace(`${currentAuthor}: `, '');
				const currentRating = li.querySelector('.review-rating').innerText.split('/')[0];

				const author = prompt("Имя автора:", currentAuthor);
				const text = prompt("Текст отзыва:", currentText);
				const rating = prompt("Рейтинг (1-10):", currentRating);

				if (!author || !text || !rating) return;

				const formData = new FormData();
				formData.append('author', author);
				formData.append('text', text);
				formData.append('rating', rating);

				try {
					const res = await fetch(`/review/${reviewId}/edit`, { method: 'POST', body: formData });
					const data = await res.json();
					if (data.success) {
						await loadReviews(filmId, 1);
					} else {
						alert('Ошибка при редактировании отзыва.');
					}
				} catch (err) {
					console.error('Ошибка редактирования отзыва:', err);
				}
			};
		});

		reviewsList.querySelectorAll('.delete-review').forEach(btn => {
			btn.onclick = async (e) => {
				e.stopPropagation();
				if (!confirm("Удалить этот отзыв?")) return;

				const li = btn.closest('li');
				const reviewId = li.dataset.reviewId;

				try {
					const res = await fetch(`/review/${reviewId}/delete`, { method: 'POST' });
					const data = await res.json();
					if (data.success) {
						li.remove();
						if (!reviewsList.children.length) {
							reviewsList.innerHTML = '<li>Пока нет отзывов.</li>';
						}
					} else {
						alert('Ошибка при удалении отзыва.');
					}
				} catch (err) {
					console.error('Ошибка удаления отзыва:', err);
				}
			};
		});
	}

	document.querySelectorAll('.film-card').forEach(card => {
		card.addEventListener('click', async (event) => {
			if (event.target.closest('button, form')) return;

			currentFilmId = card.dataset.filmId;

			try {
				const response = await fetch(`/api/film/${currentFilmId}`);
				if (!response.ok) return;
				const film = await response.json();

				const setText = (id, value) => { const el = document.getElementById(id); if (el) el.innerText = value; };
				const setSrc = (id, src) => { const el = document.getElementById(id); if (el) el.src = src; };

				setSrc('filmPoster', `/static/images/${film.image_url}`);
				setText('filmTitle', film.title);
				setText('filmOrigTitle', film.orig_title);
				setText('filmDesc', film.descr);
				setText('filmAge', film.age_rate);
				setText('filmYear', film.release_year);
				setText('filmDuration', film.duration);
				setText('filmGenres', film.genres.map(g => g.genre_name).join(', '));
				setText('filmRating', film.rating);

				currentReviewPage = 1;
				loadingReviews = false;
				await loadReviews(currentFilmId, currentReviewPage);

				const addReviewForm = document.getElementById('addReviewForm');
				if (addReviewForm) {
					addReviewForm.dataset.filmId = currentFilmId;
					addReviewForm.reset();
				}

				modal.style.display = "block";

				const reviewsList = document.getElementById('filmReviews');
				if (reviewsList) {
					reviewsList.onscroll = async () => {
						if (loadingReviews) return;
						if (reviewsList.scrollTop + reviewsList.clientHeight >= reviewsList.scrollHeight - 5) {
							loadingReviews = true;
							currentReviewPage += 1;
							await loadReviews(currentFilmId, currentReviewPage);
							loadingReviews = false;
						}
					};
				}

			} catch (err) {
				console.error('Ошибка загрузки фильма:', err);
			}
		});
	});

	Array.from(closeButtons).forEach(btn => { btn.onclick = () => { if(modal) modal.style.display = "none"; }; });
	window.onclick = (event) => { modals.forEach(m => { if (event.target === m) m.style.display = "none"; }); };

	const addReviewForm = document.getElementById('addReviewForm');
	if (addReviewForm) {
		addReviewForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			const filmId = addReviewForm.dataset.filmId;
			const formData = new FormData(addReviewForm);

			try {
				const response = await fetch(`/film/${filmId}/add_review`, { method: 'POST', body: formData });
				if (!response.ok) { alert('Ошибка при добавлении отзыва.'); return; }

				const data = await response.json();
				await loadReviews(filmId, 1);
				addReviewForm.reset();

			} catch (err) {
				console.error('Ошибка при добавлении отзыва:', err);
			}
		});
	}
});