import json

import requests
from flask import redirect
from flask import render_template, Flask, request
from os import environ

from models.db import Categories, SingleRoom, Rooms

app = Flask(__name__)
app.config.setdefault('DATABASE_URI', environ.get('DATABASE_URI'))
app.config.setdefault('API_KEY', environ.get('API_KEY'))

@app.route('/')
def room_index_view(*args, **kwargs):
    error = request.args.get('error')
    context = {
        'categories': Categories().get_with_rooms(),
        'error': error == 'true'
    }
    return render_template('index.html', **context)


@app.route('/room/<int:room_id>')
def single_room_view(room_id):
    context = {
        'room': SingleRoom(room_id).get(params={"depth": 1})
    }

    return render_template('room.html', **context)


@app.route('/create_room', methods=['GET', 'POST'])
def create_room_view():
    if request.method == 'POST':
        body = {
            'name': request.form['room_name'],
            'url': 'http://appear.in/' + request.form['room_name'],
            'category_id': request.form['category']
        }
        try:
            data = Rooms().post(data=body)
        except requests.exceptions.HTTPError:
            return redirect("/?error=true", code=302)
        else:
            room_id = data.split('/')[-1]
            return redirect("/room/%s" % room_id, code=302)


if __name__ == '__main__':
    app.run(
        # host='0.0.0.0', port='8081'
    )

