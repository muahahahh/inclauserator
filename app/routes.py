from app import app
from flask import render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from app import sql_generators as s

class InputForm(FlaskForm):
    inclause_field_name = StringField('Database column name')
    inclause_excel = TextAreaField('Paste excel data here',
                         validators = [InputRequired()])
    inclause_submit = SubmitField('Generate list')
    #_________________________________________________________________________________________
    case_when_then_pattern = TextAreaField("Pattern (e.g. WHEN tb.one_column = col1 AND tb.another_column = col2 THEN 'True')",
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

    if request.method == 'POST' and 'inclause_submit' in request.form:
        returned_string = s.inclaused_statement(request.form.get('inclause_excel'), request.form.get('inclause_field_name'))
        return render_template('results_page.html',
                               result=returned_string)

    if request.method == 'POST' and 'case_when_then_submit' in request.form:
        returned_string = s.case_statement(request.form.get('case_when_then_pattern'),
                             request.form.get('case_when_then_inclause_excel'),
                             request.form.get('case_when_then_else'))
        return render_template('results_page.html',
                               result=returned_string)

    if request.method == 'POST' and 'insertor_submit' in request.form:
        create_string = s.create_statement(request.form.get('insertor_table_name'),
                             request.form.get('insertor_excel'))
        insert_string = s.insert_statement(request.form.get('insertor_table_name'),
                             request.form.get('insertor_excel'))

        returned_string = create_string + '\n\n' + insert_string
        return render_template('results_page.html',
                               result=returned_string)

    return render_template('inclauserator.html',
                           form=form)



