from app import app
from flask import render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

class InputForm(FlaskForm):
    field_name = StringField('Database column name')
    excel = TextAreaField('Paste excel data here',
                         validators = [InputRequired()])
    submit = SubmitField('Generate list')


@app.route('/', methods=['GET', 'POST'])
def form():
    form = InputForm()

    if request.method == "POST":
        inclaused = join_newline(request.form.get('excel'), request.form.get('field_name'))
        print(inclaused)
        return render_template('results_page.html',
                               result=inclaused)

    return render_template('inclauserator.html',
                           form=form)


def join_newline(list_of_values, field_name):
    list_of_values = list(set(list_of_values.splitlines()))
    row = ''
    sep = ', '
    for i, v in enumerate(list_of_values):
        length = len(row + sep + v)
        row = row + sep + v
        if length >= 79:
            print('added')
            list_of_values.insert(i, "\n")
            length = 0
            row = ''

    string = ', '.join( ("'{0}'".format(v) if v != "\n" else "\n" ) for v in list_of_values)
    string = str(field_name) + " in (" + string.replace(", \n,", ",\n") + ")"
    return string







