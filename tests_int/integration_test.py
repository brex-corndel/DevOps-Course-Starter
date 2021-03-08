import pytest
from unittest.mock import patch, Mock
from dotenv import find_dotenv, load_dotenv
from todo_app.app import create_app
import os

@pytest.fixture 
def client():
# Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True) 

    # Create the test app
    test_app = create_app() 

    # Use the app to create a test_client that can be used in our tests.

    with test_app.test_client() as client: 
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):

    mock_get_requests.side_effect = mock_get_lists 
    response = client.get('/') 
    assert 'A card' in response.data.decode()


def mock_get_lists(url, params):
    sample_trello_lists_response = [
        {
            "name": "A card",
            "id": "daisdhksdhkhksdjhkjasdh",
            "idList": os.getenv("TRELLO_TODO_LIST_ID"),
            "dateLastActivity": "2017-02-16T13:00:21.457Z",
        },
        {
            "name": "A card",
            "id": "daisdhksdhkhksdjhkjasdh",
            "idList": os.getenv("TRELLO_TODO_LIST_ID"),
            "dateLastActivity": "2017-02-16T13:00:21.457Z",
        }
    ]

    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    if url == f'https://api.trello.com/1/boards/{trello_board_id}/cards':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_lists_response
        return response 
    return None