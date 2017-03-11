import json
from flask import render_template, Flask, request

from models.db import Categories, SingleRoom, Rooms

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def room_index_view():
    context = {
        'categories': Categories().get_with_rooms()
    }
    return render_template('index.html', **context)


@app.route('/room/<int:room_id>')
def single_room_view(room_id):
    context = {
        'room': SingleRoom(room_id).get()
    }

    return render_template('room.html', **context)


@app.route('/create_room', methods=['GET', 'POST'])
def create_room_view():
    if request.method == 'GET':
        context = {
            'categories': Categories().get()
        }
        print(context)
        return render_template('create_room.html', **context)

    if request.method == 'POST':
        body = {
            'name': request.form['room_name'],
            'url': 'http://appear.in/' + request.form['room_name'],
            'category_id': request.form['category']
        }
        Rooms().post(data=body)
        return 'ok'


if __name__ == '__main__':
    app.run(
        # host='0.0.0.0', port='8081'
    )

