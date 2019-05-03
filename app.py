import os
from flask import Flask, render_template, request, session, url_for, redirect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm


#DATABASE CONFIG FILE
projectdir = os.path.dirname(os.path.abspath(__file__))
databasefile = "sqlite:///{}".format(os.path.join(projectdir, 'notes.db'))

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'bernardisawesome'
app.config['SQLALCHEMY_DATABASE_URI'] = databasefile
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    note = db.Column(db.String(128))
    
    def __init__(self, title, note):
        self.title = title
        self.note = note
        
    def __repr__(self):
        return "<Note: {}".format(self.note)

class NotesForm(FlaskForm):
    title = StringField('Enter the title of your notes', validators=[DataRequired(), Length(min=3, max=20)])
    notes = TextAreaField('Enter your notes', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Save')

@app.route('/')
def index():
    form = NotesForm()
    allnotes = Notes.query.all()
    return render_template('index.html', form=form, allnotes = allnotes)

@app.route('/addnotes', methods=['GET', 'POST'])
def addnotes():
    form = NotesForm()
    if request.method == 'POST':
        note = Notes(title=form.title.data, note=form.notes.data)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NotesForm()
    allnotes = Notes.query.all()
    return render_template('notes.html', allnotes=allnotes, form=form)

@app.route('/delete/<string:id>/', methods=['GET', 'POST'])
def delete(id):
    allnotes = Notes.query.filter_by(id=id).first()
    db.session.delete(allnotes)
    db.session.commit()
    return redirect(url_for('notes'))


if __name__ == '__main__':
    app.run(debug=True)