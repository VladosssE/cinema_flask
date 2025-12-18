def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_film_visible_on_page(client, film):
    html = client.get("/").get_data(as_text=True)
    assert "Тестовый фильм" in html


def test_original_title_visible(client, film):
    html = client.get("/").get_data(as_text=True)
    assert "Test Movie" in html


def test_genre_visible(client, genre):
    html = client.get("/").get_data(as_text=True)
    assert "Драма" in html


def test_search_found(client, film):
    html = client.get("/?q=Тестовый").get_data(as_text=True)
    assert "Тестовый фильм" in html


def test_search_not_found(client, film):
    html = client.get("/?q=Несуществующий").get_data(as_text=True)
    assert "Тестовый фильм" not in html


def test_page_header(client):
    html = client.get("/").get_data(as_text=True)
    assert "<h2>Фильмы</h2>" in html


def test_search_form_exists(client):
    html = client.get("/").get_data(as_text=True)
    assert "Поиск фильма" in html
