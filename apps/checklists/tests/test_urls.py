from django.urls import reverse


def test_checklists_list_url(db_no_rollback, client):
    url = reverse("checklists:list")
    assert client.get(url).status_code == 200


def test_checklists_detail_url(db_no_rollback, client, checklist):
    headers = {'HTTP_REFERER': reverse("checklists:list")}
    url = reverse("checklists:detail", kwargs={"identifier": checklist.identifier})
    assert client.get(url, **headers).status_code == 200
