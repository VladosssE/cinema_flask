document.addEventListener("DOMContentLoaded", () => {
    const filterSortModal = document.getElementById("filterSortModal");
    const openFilterSortBtn = document.getElementById("filterSortBtn");
    const closeFilterSortBtn = document.getElementById("closeFilterSort");
    const filterSortForm = document.getElementById("filterSortForm");
    const filmContainer = document.querySelector(".films-container");
    const originalFilms = Array.from(document.querySelectorAll(".film-card"));

    if (openFilterSortBtn) {
        openFilterSortBtn.addEventListener("click", () => {
            filterSortModal.style.display = "block";
        });
    }

    if (closeFilterSortBtn) {
        closeFilterSortBtn.addEventListener("click", () => {
            filterSortModal.style.display = "none";
        });
    }

    window.addEventListener("click", (e) => {
        if (e.target === filterSortModal) filterSortModal.style.display = "none";
    });

    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape") filterSortModal.style.display = "none";
    });

    const sortSelect = document.getElementById("sortBy");
    const genreSelect = document.getElementById("filterGenre");
    const ageSelect = document.getElementById("filterAge");

    function applyFilterSort() {
        const genre = genreSelect.value;
        const age = ageSelect.value;
        const sortBy = sortSelect.value;

        let filtered = originalFilms.filter(f => {
            const filmGenres = f.dataset.genres ? f.dataset.genres.split(",").map(g => g.trim()) : [];
            const filmAge = f.dataset.ageRate || "";
            return (genre === "" || filmGenres.includes(genre)) &&
                   (age === "" || filmAge === age);
        });

        if (sortBy) {
            const [sortKey, sortDirRaw] = sortBy.split("_");
            const sortDir = sortDirRaw === "asc" ? 1 : -1;

            filtered.sort((a, b) => {
                let valA, valB;

                if (sortKey === "title") {
                    valA = a.querySelector(".film-title").textContent.toLowerCase();
                    valB = b.querySelector(".film-title").textContent.toLowerCase();
                    return valA.localeCompare(valB) * sortDir;
                }

                if (sortKey === "rating") {
                    valA = parseFloat(a.querySelector(".film-rating .rating").textContent.replace(/[^\d.]/g,"")) || 0;
                    valB = parseFloat(b.querySelector(".film-rating .rating").textContent.replace(/[^\d.]/g,"")) || 0;
                    return (valA - valB) * sortDir;
                }

                if (sortKey === "year") {
                    valA = parseInt(a.dataset.releaseYear) || 0;
                    valB = parseInt(b.dataset.releaseYear) || 0;
                    return (valA - valB) * sortDir;
                }

                return 0;
            });
        }

        filmContainer.innerHTML = "";
        filtered.forEach(f => filmContainer.appendChild(f));
    }

    function resetFilters() {
        sortSelect.value = "";
        genreSelect.value = "";
        ageSelect.value = "";
        filmContainer.innerHTML = "";
        originalFilms.forEach(f => filmContainer.appendChild(f));
    }

    if (filterSortForm) {
        filterSortForm.addEventListener("submit", (e) => {
            e.preventDefault();
            applyFilterSort();
            filterSortModal.style.display = "none";
        });

        const resetBtn = document.createElement("button");
        resetBtn.textContent = "Сбросить фильтры и сортировку";
        resetBtn.type = "button";
        resetBtn.style.marginTop = "10px";
        resetBtn.className = "add-film-special";
        resetBtn.addEventListener("click", resetFilters);
        filterSortForm.appendChild(resetBtn);
    }
});