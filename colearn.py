from flask import render_template, Flask

from models.db import Categories, SingleRoom

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    context = {
        'categories': Categories().get_with_rooms()
    }
    return render_template('index.html', **context)

@app.route('/room/<int:room_id>')
def single_room_view(room_id):
    context = {
        'room': SingleRoom(1).get()
    }

    return render_template('room.html', **context)


if __name__ == '__main__':
    app.run()
