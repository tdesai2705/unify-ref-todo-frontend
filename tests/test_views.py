import os
import pytest
from unittest.mock import patch, MagicMock
import requests as req_lib
from app import create_app


@pytest.fixture
def app():
    os.environ['BACKEND_API_URL'] = 'http://mock-backend:5000'
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret'
    yield app
    del os.environ['BACKEND_API_URL']


@pytest.fixture
def client(app):
    return app.test_client()


MOCK_TODOS = [
    {'id': 1, 'title': 'Buy groceries', 'completed': False, 'priority': 'high', 'category': 'personal', 'user_id': 1, 'description': '', 'due_date': None, 'created_at': '2026-06-10T00:00:00'},
    {'id': 2, 'title': 'Write tests', 'completed': True, 'priority': 'medium', 'category': 'work', 'user_id': 1, 'description': '', 'due_date': None, 'created_at': '2026-06-10T00:00:00'},
]

MOCK_STATS = {
    'total': 2,
    'completed': 1,
    'pending': 1,
    'completion_rate': 50.0,
    'by_priority': {'high': 1, 'medium': 1, 'low': 0}
}


def make_mock_response(data, status_code=200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = data
    return mock


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'todo-frontend'


def test_root_redirects_to_todos(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/todos' in response.headers['Location']


def test_todo_list_renders(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.side_effect = [
            make_mock_response(MOCK_TODOS),
            make_mock_response(MOCK_STATS),
        ]
        response = client.get('/todos')
        assert response.status_code == 200
        assert b'Buy groceries' in response.data
        assert b'Write tests' in response.data


def test_todo_list_shows_stats(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.side_effect = [
            make_mock_response(MOCK_TODOS),
            make_mock_response(MOCK_STATS),
        ]
        response = client.get('/todos')
        assert response.status_code == 200
        assert b'50' in response.data


def test_todo_list_backend_error_shows_empty(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.side_effect = req_lib.exceptions.ConnectionError('Connection refused')
        response = client.get('/todos')
        assert response.status_code == 200


def test_add_todo_success(client):
    with patch('app.views.requests.post') as mock_post:
        mock_post.return_value = make_mock_response(
            {'id': 3, 'title': 'New task', 'completed': False, 'priority': 'medium', 'user_id': 1},
            status_code=201
        )
        response = client.post('/todos/add', data={
            'title': 'New task',
            'priority': 'medium',
            'category': 'work'
        }, follow_redirects=False)
        assert response.status_code == 302


def test_add_todo_backend_error(client):
    with patch('app.views.requests.post') as mock_post:
        mock_post.side_effect = req_lib.exceptions.ConnectionError('Connection refused')
        response = client.post('/todos/add', data={'title': 'Fail task'}, follow_redirects=False)
        assert response.status_code == 302


def test_toggle_todo_success(client):
    with patch('app.views.requests.get') as mock_get, \
         patch('app.views.requests.put') as mock_put:
        mock_get.return_value = make_mock_response(MOCK_TODOS[0])
        mock_put.return_value = make_mock_response({**MOCK_TODOS[0], 'completed': True})
        response = client.post('/todos/1/toggle', follow_redirects=False)
        assert response.status_code == 302


def test_toggle_todo_not_found(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.return_value = make_mock_response({}, status_code=404)
        response = client.post('/todos/999/toggle', follow_redirects=False)
        assert response.status_code == 302


def test_delete_todo_success(client):
    with patch('app.views.requests.delete') as mock_delete:
        mock_delete.return_value = make_mock_response(None, status_code=204)
        response = client.post('/todos/1/delete', follow_redirects=False)
        assert response.status_code == 302


def test_delete_todo_backend_error(client):
    with patch('app.views.requests.delete') as mock_delete:
        mock_delete.return_value = make_mock_response({'error': 'Not found'}, status_code=404)
        response = client.post('/todos/999/delete', follow_redirects=False)
        assert response.status_code == 302


def test_feature_flag_env_var_off(client):
    with patch.dict(os.environ, {'FEATURE_DUE_DATE': 'false', 'FEATURE_DARK_MODE': 'false'}):
        with patch('app.views.requests.get') as mock_get:
            mock_get.side_effect = [
                make_mock_response(MOCK_TODOS),
                make_mock_response(MOCK_STATS),
            ]
            response = client.get('/todos')
            assert response.status_code == 200


def test_feature_flag_env_var_on(client):
    with patch.dict(os.environ, {'FEATURE_DUE_DATE': 'true', 'FEATURE_DARK_MODE': 'true'}):
        with patch('app.views.requests.get') as mock_get:
            mock_get.side_effect = [
                make_mock_response(MOCK_TODOS),
                make_mock_response(MOCK_STATS),
            ]
            response = client.get('/todos')
            assert response.status_code == 200


def test_todo_list_filter_by_priority(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.side_effect = [
            make_mock_response([MOCK_TODOS[0]]),
            make_mock_response(MOCK_STATS),
        ]
        response = client.get('/todos?priority=high')
        assert response.status_code == 200
        assert b'Buy groceries' in response.data


def test_todo_list_filter_by_completed(client):
    with patch('app.views.requests.get') as mock_get:
        mock_get.side_effect = [
            make_mock_response([MOCK_TODOS[1]]),
            make_mock_response(MOCK_STATS),
        ]
        response = client.get('/todos?completed=true')
        assert response.status_code == 200
        assert b'Write tests' in response.data
