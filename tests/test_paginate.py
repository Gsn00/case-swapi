from main import paginate

def test_paginate():
    data = list(range(25))
    page = 1

    paginated = paginate(data, page)
    assert len(paginated['results']) == 10
    assert paginated['next_page'] == '?page=2'
    assert paginated['previous_page'] is None