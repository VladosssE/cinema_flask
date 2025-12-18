document.addEventListener('DOMContentLoaded', () => {
	const modal = document.getElementById("filmInfo");
	const span = document.getElementsByClassName("close")[0];
	const modals = document.querySelectorAll('.modal');

	let currentReviewPage = 1;
	let loadingReviews = false;

	async function loadReviews(filmId, page = 1) {
		const reviewsList = document.getElementById('filmReviews');
		if (!reviewsList) return;

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
			li.innerHTML = `
				<span class="review-text"><strong>${r.author}:</strong> ${r.text}</span>
				<span class="review-rating">${r.rating}/10</span>
			`;
			reviewsList.appendChild(li);
		});
	}

	document.querySelectorAll('.film-card').forEach(card => {
		card.addEventListener('click', async function (event) {
			if (event.target.closest('button, form')) return;

			const filmId = this.dataset.filmId;
			const response = await fetch(`/api/film/${filmId}`);
			const film = await response.json();

			document.getElementById('filmPoster').src = `/static/images/${film.image_url}`;
			document.getElementById('filmTitle').innerText = film.title;
			document.getElementById('filmOrigTitle').innerText = film.orig_title;
			document.getElementById('filmDesc').innerText = film.descr;
			document.getElementById('filmAge').innerText = film.age_rate;
			document.getElementById('filmYear').innerText = film.release_year;
			document.getElementById('filmDuration').innerText = film.duration;
			document.getElementById('filmGenres').innerText = film.genres.map(g => g.genre_name).join(', ');
			document.getElementById('filmRating').innerText = film.rating;

			currentReviewPage = 1;
			loadingReviews = false;
			await loadReviews(filmId, currentReviewPage);

			const addReviewForm = document.getElementById('addReviewForm');
			if (addReviewForm) {
				addReviewForm.dataset.filmId = filmId;
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
						await loadReviews(filmId, currentReviewPage);
						loadingReviews = false;
					}
				};
			}
		});
	});

	span.onclick = () => { modal.style.display = "none"; };
	window.onclick = (event) => {
		modals.forEach(modal => {
			if (event.target === modal) modal.style.display = "none";
		});
	};

	const addReviewForm = document.getElementById('addReviewForm');
	if (addReviewForm) {
		addReviewForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			const filmId = e.target.dataset.filmId;
			const formData = new FormData(e.target);

			const response = await fetch(`/film/${filmId}/add_review`, {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				const author = formData.get('author');
				const text = formData.get('text');
				const rating = formData.get('rating');

				const reviewsList = document.getElementById('filmReviews');
				if (!reviewsList) return;

				const li = document.createElement('li');
				li.classList.add('review-item');
				li.innerHTML = `
					<span class="review-text"><strong>${author}:</strong> ${text}</span>
					<span class="review-rating">${rating}/10</span>
				`;

				if (reviewsList.children.length === 1 && reviewsList.children[0].innerText === 'Пока нет отзывов.') {
					reviewsList.innerHTML = '';
				}
				reviewsList.appendChild(li);

				e.target.reset();
			} else {
				alert('Ошибка при добавлении отзыва.');
			}
		});
	}
});