document.addEventListener("DOMContentLoaded", () => {
	const addFilmModal = document.getElementById("addFilmModal");
	const openAddFilm = document.getElementById("openAddFilm");
	const closeAddFilm = document.getElementById("closeAddFilm");
	const modals = document.querySelectorAll('.modal');
	

	if(openAddFilm){
		openAddFilm.onclick = () => {
			if(addFilmModal){
				addFilmModal.style.display = "block";
			}
		}
	}

	if(closeAddFilm){
		closeAddFilm.onclick = () => {
			if(addFilmModal){
				addFilmModal.style.display = "none";
			}
		}
	}
	 

	window.onclick = (event) => {
		modals.forEach(modal => {
			if (event.target === modal) {
				modal.style.display = "none";
 			}
		});
	};

	if(addFilmModal){
		const form = addFilmModal.querySelector('form');
		if(form){
			form.onsubmit = async (e) => {
				e.preventDefault();
				const formData = new FormData(form);
				const data = Object.fromEntries(formData.entries());

				const genres = Array.from(document.getElementById('genreSelect').selectedOptions).map(opt => opt.value);
				data.genres = genres;

				try{
					const response = await fetch("/api/film/add", {
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify(data)
					});

					const result = await response.json();
					if (result.success) {
						location.reload();
					} else {
						alert("Ошибка при добавлении фильма");
					}
				}catch(err){
					alert("Произошла ошибка при отправке формы");
				}
			};
		}
	}
});