from django.urls import reverse


def test_list_view__is_paginated(db_no_rollback, client):
    url = reverse("checklists:list")
    response = client.get(url)
    view = response.context["view"]
    assert view.paginate_by is not None


def test_detail_view__checklist_displayed(db_no_rollback, client, checklist):
    headers = {'HTTP_REFERER': reverse("checklists:list")}
    url = reverse("checklists:detail", kwargs={"identifier": checklist.identifier})
    response = client.get(url, **headers)
    assert response.context["object"] == checklist
