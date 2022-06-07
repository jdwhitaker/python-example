from flask import (
    Flask, 
    render_template, 
    make_response,
    session,
    redirect,
    url_for,
    flash
)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import datetime
from wtforms import (
    StringField, 
    SubmitField
)
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{database}".format(
    username = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASSWORD'),
    hostname = os.getenv('MYSQL_HOSTNAME'),
    database = os.getenv('MYSQL_DATABASE'),
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardcoded-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class Widget(db.Model):
    __tablename__ = 'widgets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, index=True)
    value = db.Column(db.String(256))
    reviews = db.relationship('Review', backref='role')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text())
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))

db.create_all()

@app.route('/')
def index():
    response = make_response()
    response.status_code = 200
    response_data = render_template('index.html', current_time = datetime.datetime.utcnow())
    response.set_data(response_data)
    return response

@app.route('/widget/<string:name>')
def readWidget(name):
    widget = Widget.query.filter_by(name=name).first()
    if widget == None:
        flash("Widget not found")
        response = make_response()
        response.status_code = 200
        response_data = render_template('readWidget.html', widget=widget)
        response.set_data(response_data)
        return response
    else:
        response = make_response()
        response.status_code = 200
        response_data = render_template('readWidget.html', widget=widget)
        response.set_data(response_data)
        return response


@app.route('/createWidget', methods=['GET','POST'])
def createWidget():
    form = WidgetForm()
    if form.validate_on_submit():
        name = form.name.data
        value = form.value.data
        widget = Widget(name=name, value=value)
        try:
            db.session.add(widget)
            db.session.commit()
            flash("Created widget '{widget_name}'".format(widget_name=name))
        except:
            flash("Widget '{widget_name}' already exists".format(widget_name=name))
        return redirect(url_for('createWidget'))
    return render_template('createWidget.html', form=form)

class WidgetForm(FlaskForm):
    name = StringField("Widget Name", validators=[DataRequired()])
    value = StringField("Widget Value", validators=[DataRequired()])
    submit = SubmitField('Submit')

