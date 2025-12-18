document.addEventListener('DOMContentLoaded', function() {
	const posterSelect = document.getElementById('posterSelect');
	const img = document.getElementById('posterPreview');

	function updatePoster(filename) {
		if (filename) {
			img.src = '/static/images/' + filename;
		} else {
			img.src = '/static/images/placeholder.jpg';
		}
	}

	posterSelect.addEventListener('change', function() {
		updatePoster(this.value);
	});
	updatePoster(posterSelect.value);
});