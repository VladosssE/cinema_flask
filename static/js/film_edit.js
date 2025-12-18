let editSelectedGenres = new Set();
let currentFilmId = null;

function openEditFilm(filmId) {
	currentFilmId = filmId;
	const modal = document.getElementById('editFilmModal');
	modal.style.display = 'block';

	const filmCard = document.querySelector(`.film-card[data-film-id='${filmId}']`);
	const title = filmCard.querySelector('.film-title').textContent;
	const origTitle = filmCard.querySelector('.orig-film-title').textContent;
	const releaseYear = filmCard.getAttribute('data-release-year');
	const ageRate = filmCard.getAttribute('data-age-rate');
	const duration = filmCard.getAttribute('data-duration') || '';
	const descr = filmCard.getAttribute('data-descr') || '';
	const imageUrl = filmCard.querySelector('.film-poster').getAttribute('src').replace('/static/images/', '');

	document.getElementById('editTitle').value = title;
	document.getElementById('editOrigTitle').value = origTitle;
	document.getElementById('editYear').value = releaseYear;
	document.getElementById('editAge').value = ageRate;
	document.getElementById('editDuration').value = duration;
	document.getElementById('editDesc').value = descr;

	const posterSelect = document.getElementById('editPosterSelect');
	const posterPreview = document.getElementById('editPosterPreview');
	posterPreview.src = `/static/images/${imageUrl}`;
	posterSelect.value = imageUrl;

	editSelectedGenres.clear();
	const genreIds = filmCard.getAttribute('data-genres').split(',');
	genreIds.forEach(id => editSelectedGenres.add(id));
	document.getElementById('editSelectedGenres').value = Array.from(editSelectedGenres).join(',');

	const genreButtons = document.querySelectorAll('#editGenreButtons .genre-btn');
	genreButtons.forEach(btn => {
		btn.classList.toggle('selected', editSelectedGenres.has(btn.dataset.id));

		btn.onclick = () => {
			if (editSelectedGenres.has(btn.dataset.id)) {
				editSelectedGenres.delete(btn.dataset.id);
				btn.classList.remove('selected');
			} else {
				editSelectedGenres.add(btn.dataset.id);
				btn.classList.add('selected');
			}
			document.getElementById('editSelectedGenres').value = Array.from(editSelectedGenres).join(',');
		};
	});

	const toggleGenres = document.getElementById('editToggleGenres');
	toggleGenres.onclick = () => {
		document.getElementById('editGenreButtons').classList.toggle('collapsed');
	};

	posterSelect.onchange = () => {
		posterPreview.src = posterSelect.value ? `/static/images/${posterSelect.value}` : '/static/images/placeholder.jpg';
	};
}

function closeEditFilm() {
	document.getElementById('editFilmModal').style.display = 'none';
}

window.onclick = function(event) {
	const modal = document.getElementById('editFilmModal');
	if (event.target === modal) {
		closeEditFilm();
	}
};

document.getElementById('editFilmForm').onsubmit = function(e) {
	e.preventDefault();

	if (!currentFilmId) {
		alert('Не выбран фильм для редактирования');
		return;
	}

	const data = {
		title: document.getElementById('editTitle').value,
		orig_title: document.getElementById('editOrigTitle').value,
		descr: document.getElementById('editDesc').value,
		release_year: document.getElementById('editYear').value,
		duration: document.getElementById('editDuration').value,
		age_rate: document.getElementById('editAge').value,
		image_url: document.getElementById('editPosterSelect').value,
		genres: Array.from(editSelectedGenres).map(Number)
	};

	fetch(`/api/film/${currentFilmId}/edit`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	})
	.then(res => res.json())
	.then(res => {
		if (res.success) {
			location.reload();
		} else {
			alert('Ошибка при обновлении фильма');
		}
	})
	.catch(err => {
		console.error(err);
		alert('Ошибка при запросе к серверу');
	});
};