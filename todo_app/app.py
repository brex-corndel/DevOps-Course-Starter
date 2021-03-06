from flask import Flask, render_template, request, redirect, url_for

import todo_app.trello_client as trello_client
from todo_app.view_model import ViewModel
from todo_app.data.todo_item import TodoItem

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        raw_cards = trello_client.get_cards_for_board()
        todo_items = [TodoItem.from_raw_trello_card(card) for card in raw_cards]
        item_view_model = ViewModel(todo_items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add_item', methods=['POST'])
    def add_item():
        item_title = request.form['Title']
        trello_client.add_todo(item_title)
        return redirect('/')

    @app.route('/complete_item', methods=['POST'])
    def complete_item():
        todo_id = request.form['id']
        trello_client.complete_todo(todo_id)
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run()


