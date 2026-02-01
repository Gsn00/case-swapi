from main import filter_films, filter_planets, filter_people, filter_starships

def test_filter_planets():
    data = [{
      "climate": "arid",
      "id": "1",
      "name": "Tatooine",
      "population": "200000",
      "terrain": "desert"
    },
    {
      "climate": "temperate",
      "id": "2",
      "name": "Alderaan",
      "population": "2000000000",
      "terrain": "grasslands, mountains"
    }]

    args = {'name': 'ta'}

    filtered = filter_planets(data, args)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Tatooine'

def test_filter_people():
    data = [{
      "birth_year": "19BBY",
      "films": "1, 2, 3, 6",
      "gender": "male",
      "id": "1",
      "name": "Luke Skywalker"
    },
    {
      "birth_year": "112BBY",
      "films": "1, 2, 3, 4, 5, 6",
      "gender": "n/a",
      "id": "2",
      "name": "C-3PO"
    }]

    args = {'name': 'luke'}

    filtered = filter_people(data, args)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Luke Skywalker'

def test_filter_films():
    data = [{
      "characters": "1, 2, 3",
      "episode_id": 4,
      "id": "1",
      "release_date": "1977-05-25",
      "title": "A New Hope"
    },
    {
      "characters": "1, 2, 3",
      "episode_id": 5,
      "id": "2",
      "release_date": "1980-05-17",
      "title": "The Empire Strikes Back"
    }]
    args = {'title': 'empire'}

    filtered = filter_films(data, args)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'The Empire Strikes Back'

def test_filter_starships():
    data = [{
      "id": "2",
      "manufacturer": "Corellian Engineering Corporation",
      "model": "CR90 corvette",
      "name": "CR90 corvette",
      "pilots": ""
    },
    {
      "id": "3",
      "manufacturer": "Kuat Drive Yards",
      "model": "Imperial I-class Star Destroyer",
      "name": "Star Destroyer",
      "pilots": ""
    }]
    args = {'name': 'star'}

    filtered = filter_starships(data, args)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Star Destroyer'