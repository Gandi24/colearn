from flask import render_template, Flask

from models.db import Categories

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    context = {
        'categories': Categories().get_with_rooms()
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run()
