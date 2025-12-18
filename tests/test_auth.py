def test_add_film_requires_login(client):
    response = client.post("/api/film/add", json={})
    assert response.status_code in (401, 302)


def test_edit_film_requires_login(client, film):
    response = client.post(f"/api/film/{film.film_id}/edit", json={})
    assert response.status_code in (401, 302)


def test_delete_film_requires_login(client, film):
    response = client.post(f"/film/{film.film_id}/delete")
    assert response.status_code in (401, 302)
