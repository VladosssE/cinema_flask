def test_api_film_detail(client, film):
    response = client.get(f"/api/film/{film.film_id}")
    data = response.get_json()

    assert data["title"] == "Тестовый фильм"


def test_api_film_not_found(client):
    response = client.get("/api/film/999")
    assert response.status_code == 404


def test_api_release_year_format(client, film):
    data = client.get(f"/api/film/{film.film_id}").get_json()
    assert data["release_year"] == "2020-01-01"


def test_api_genres_returned(client, film):
    data = client.get(f"/api/film/{film.film_id}").get_json()
    assert len(data["genres"]) == 1


def test_api_reviews_empty(client, film):
    data = client.get(f"/api/film/{film.film_id}").get_json()
    assert data["reviews"] == []


def test_api_rating_is_string(client, film):
    data = client.get(f"/api/film/{film.film_id}").get_json()
    assert isinstance(data["rating"], str)


def test_api_contains_image_url(client, film):
    data = client.get(f"/api/film/{film.film_id}").get_json()
    assert data["image_url"] == "test.jpg"
