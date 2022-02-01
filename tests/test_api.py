import json
import testutils

FAIL_CODE = 400
SUCCESS_CODE = 200


def test_ping(client):
    res = client.get('/api/ping')
    assert res.status_code == SUCCESS_CODE
    expected = {'success': True}
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_valid_single_tag(client):
    res = client.get('/api/posts?tags=tech')
    assert res.status_code == SUCCESS_CODE
    expected = testutils.import_json('tech_tag.json')
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_valid_multiple_tags(client):
    res = client.get('/api/posts?tags=tech,science,history,startups,culture,politics')
    assert res.status_code == SUCCESS_CODE
    expected = testutils.import_json('tech,science,history,startups,culture,politics_tag.json')
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_valid_sort_by_likes(client):
    res = client.get('/api/posts?tags=tech&sortBy=likes')
    assert res.status_code == SUCCESS_CODE
    expected = testutils.import_json('tech_tag_likes_sort.json')
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_valid_sort_by_popularity(client):
    res = client.get('/api/posts?tags=tech&sortBy=popularity')
    assert res.status_code == SUCCESS_CODE
    expected = testutils.import_json('tech_tag_popularity_sort.json')
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_valid_direction(client):
    res = client.get('/api/posts?tags=tech&direction=desc')
    assert res.status_code == SUCCESS_CODE
    expected = testutils.import_json('tech_tag_desc_direction.json')
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_invalid_tag(client):
    res = client.get('/api/posts?tags=')
    assert res.status_code == FAIL_CODE
    expected = {'error': 'Tags parameter is required'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_invalid_sort_by(client):
    res = client.get('/api/posts?tags=tech&sortBy=INVALID')
    assert res.status_code == FAIL_CODE
    expected = {'error': 'sortBy parameter is invalid'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_invalid_sort_by(client):
    res = client.get('/api/posts?tags=tech&sortBy=INVALID')
    assert res.status_code == FAIL_CODE
    expected = {'error': 'sortBy parameter is invalid'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_posts_invalid_direction(client):
    res = client.get('/api/posts?tags=tech&direction=INVALID')
    assert res.status_code == FAIL_CODE
    expected = {'error': 'direction parameter is invalid'}
    assert expected == json.loads(res.get_data(as_text=True))
