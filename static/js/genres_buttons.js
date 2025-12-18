document.addEventListener("DOMContentLoaded", () => {
    const genreButtons = document.querySelectorAll('.genre-btn');
    const selectedInput = document.getElementById('selectedGenres');

    genreButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('selected');

            const selected = Array.from(genreButtons)
                .filter(b => b.classList.contains('selected'))
                .map(b => b.dataset.id);

            selectedInput.value = selected.join(',');
        });
    });

    const form = document.querySelector('#addFilmModal form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        const genres = formData.get('genres').split(',').filter(g => g);

        const data = Object.fromEntries(formData.entries());
        data.genres = genres;

        fetch("/api/film/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if(result.success) location.reload();
            else alert("Ошибка при добавлении фильма");
        });
    });
});