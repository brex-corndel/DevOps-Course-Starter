import os
from dotenv import load_dotenv, find_dotenv
from threading import Thread
from selenium import webdriver 
import pytest
import requests
from todo_app import app

@pytest.fixture(scope="module") 
def driver():
    with webdriver.Firefox(executable_path='/Users/bacis/Documents/Corndel/Module-3/DevOps-Course-Starter/geckodriver') as driver:
        yield driver

def create_trello_board():
    key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_API_TOKEN")

    url = f"https://api.trello.com/1/boards/"
    params = { "key": key, "token": token, 'name': 'E2E test board' }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception(f"Wrong status on cards response: {response.status_code}")

def delete_trello_board(board_id):
    key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_API_TOKEN")

    url = f"https://api.trello.com/1/boards/{board_id}"
    params = { "key": key, "token": token }
    response = requests.delete(url, params=params)

    if response.status_code == 200:
        return
    else:
        raise Exception(f"Wrong status on cards response: {response.status_code}")


@pytest.fixture(scope="module")
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True) 
# Create the new board & update the board id environment variable

    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id 

# construct the new application

    application = app.create_app() 

# start the app in its own thread.

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

# Tear Down

    thread.join(1) 
    delete_trello_board(board_id)

def test_task_journey(driver, app_with_temp_board): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'