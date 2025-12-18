document.addEventListener('DOMContentLoaded', () => {
	const reviewsList = document.getElementById('filmReviews');
	if (!reviewsList) return;

	let currentReviewPage = 1;
	let loadingReviews = false;

	reviewsList.addEventListener('scroll', async () => {
		if (loadingReviews) return;

		if (reviewsList.scrollTop + reviewsList.clientHeight >= reviewsList.scrollHeight - 5) {
			loadingReviews = true;
			currentReviewPage += 1;

		const addReviewForm = document.getElementById('addReviewForm');
		if (!addReviewForm) return;

		const filmId = addReviewForm.dataset.filmId;
		const response = await fetch(`/api/film/${filmId}/reviews?page=${currentReviewPage}`);
		if (response.ok) {
			const newReviews = await response.json();
			if (newReviews.length > 0) {
				newReviews.forEach(r => {
					const li = document.createElement('li');
					li.classList.add('review-item');
					li.innerHTML = `
						<span class="review-text"><strong>${r.author}:</strong> ${r.text}</span>
						<span class="review-rating">${r.rating}/10</span>
						`;
					reviewsList.appendChild(li);
					});
				}
			}
		loadingReviews = false;
	}
	});
});