import os
from dotenv import load_dotenv, find_dotenv
from threading import Thread
from selenium import webdriver 
import pytest
import requests
from todo_app import app
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import time
import todo_app.trello_client as trello_client

@pytest.fixture(scope="module") 
def driver():
 #   with webdriver.Firefox() as driver:
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') 
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
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

    lists = trello_client.get_lists_for_board()

    todo_list = [list for list in lists if list["name"] == "To Do"][0]
    done_list = [list for list in lists if list["name"] == "Done"][0]

    os.environ['TRELLO_TODO_LIST_ID'] = todo_list["id"]
    os.environ['TRELLO_DONE_LIST_ID'] = done_list["id"]

# construct the new application

    application = app.create_app() 

# start the app in its own thread.

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    time.sleep(5)

    yield app

# Tear Down

    thread.join(1) 
    delete_trello_board(board_id)

def test_task_journey(driver, app_with_temp_board): 
    driver.get('http://localhost:5000/')
    driver.implicitly_wait(10)
    assert driver.title == 'To-Do App'

    title_box = driver.find_element_by_id("Title")
    title_box.send_keys("e2e Test Todo")

    title_box.send_keys(Keys.RETURN)

    driver.find_element_by_name("item-complete-button").click()

    title_element: WebElement = driver.find_element_by_name("item-title")
    status_element: WebElement = driver.find_element_by_name("item-status")
    
    assert title_element.text == "e2e Test Todo"
    assert status_element.text == "Done"
