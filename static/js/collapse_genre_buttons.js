document.addEventListener("DOMContentLoaded", () => {
	const toggle = document.getElementById("toggleGenres");
	const genres = document.getElementById("genreButtons");

	toggle.addEventListener("click", () => {
		genres.classList.toggle("collapsed");
		toggle.querySelector(".arrow").textContent =
			genres.classList.contains("collapsed") ? "+" : "-";
	});
});