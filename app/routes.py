from app import app
from flask import render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

class InputForm(FlaskForm):
    inclause_field_name = StringField('Database column name')
    inclause_excel = TextAreaField('Paste excel data here',
                         validators = [InputRequired()])
    inclause_submit = SubmitField('Generate list')
    #_________________________________________________________________________________________
    case_when_then_pattern = TextAreaField('Pattern',
                                                validators=[InputRequired()])
    case_when_then_inclause_excel = TextAreaField('Paste excel columns here',
                                   validators=[InputRequired()])
    case_when_then_else = TextAreaField('Else value',
                                                  validators=[InputRequired()])
    case_when_then_submit = SubmitField('Generate statement')
    # _________________________________________________________________________________________
    insertor_table_name = StringField('New table name', validators=[InputRequired()])
    insertor_excel = TextAreaField('Paste excel columns here',
                                   validators=[InputRequired()])
    insertor_submit = SubmitField('Generate statement')


@app.route('/', methods=['GET', 'POST'])
def form():
    form = InputForm()

    if request.method == "POST" and 'inclause_submit' in request.form:
        inclaused = inclause(request.form.get('inclause_excel'), request.form.get('inclause_field_name'))
        return render_template('results_page.html',
                               result=inclaused)
    if request.method == "POST" and 'case_when_then_submit' in request.form:
        casenated = casenate(request.form.get('case_when_then_pattern'),
                             request.form.get('case_when_then_inclause_excel'),
                             request.form.get('case_when_then_else'))
        return render_template('results_page.html',
                               result=casenated)

    return render_template('inclauserator.html',
                           form=form)


def inclause(list_of_values, field_name):
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


def casenate(pattern, excel, els):
    string = "CASE \n"
    excel = excel.split('\n')
    excel = [x for x in excel if x]
    for i in excel:
        columns = i.count('\t') + 1
        values = i.split('\t')

        statemt = pattern.replace("col{}".format(str(1)), "'" + values[0].strip() + "'")
        for x in range(2, columns + 1):
            statemt = statemt.replace("col{}".format(str(x)), "'" + values[x - 1].strip() + "'")

        string = '\t' + string + statemt
        string += '\n'

    string = string + "ELSE '{}'\nEND".format(els)
    return string






