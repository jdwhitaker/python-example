from flask import (
    Flask, 
    render_template, 
    make_response,
    session,
    redirect,
    url_for,
    flash
)
from gpg import Data
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import datetime
from wtforms import (
    StringField, 
    SubmitField
)
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardcoded-secret'
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

@app.route('/greeter', methods=['GET','POST'])
def greeter():
    form = NameForm()
    if form.validate_on_submit():
        if session.get('name') != form.name.data:
            flash('You submitted your name')
        session['name'] = form.name.data
        return redirect(url_for('greeter'))
    return render_template('greeter.html', form=form, name=session.get('name'))

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')