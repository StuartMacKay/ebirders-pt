from django.urls import reverse


def test_home_page__redirect(db_no_rollback, client):
    response = client.get("/", follow=True)
    assert len(response.redirect_chain) == 2
    assert response.redirect_chain[0] == (reverse("index"), 302)
    assert response.redirect_chain[1] == (reverse("news:index"), 302)
