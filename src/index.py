from flask import (
    Flask, 
    render_template, 
    make_response
)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    response = make_response()
    response.status_code = 200
    response_data = render_template('index.html', current_time = datetime.datetime.utcnow())
    response.set_data(response_data)
    return response

@app.route('/user/<string:name>')
def user(name):
    response = make_response()
    response.status_code = 200
    response_data = render_template('user.html', name=name)
    response.set_data(response_data)
    return response