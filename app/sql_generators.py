
from io import StringIO

import pandas as pd


def inclaused_statement(list_of_values, field_name):
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


def case_statement(pattern, excel, els):
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


def create_statement(table_name, excel):
    df = pd.read_csv(StringIO(excel), sep='\t', dtype=str).fillna('')
    string = "CREATE TABLE {} (\n".format(table_name)

    for i in list(df.columns):
        string = "{}\t{} VARCHAR({}),\n".format(string, i, df[i].map(len).max())
    string = string[:-2] + ');'
    return string


def insert_statement(table_name, excel):
    df = pd.read_csv(StringIO(excel), sep='\t', dtype=str).fillna('')
    string = "INSERT INTO {} {} VALUES \n".format(table_name, str(tuple(df.columns)).replace("'", ""))
    for i in range(len(df)):
        string = "{}\t{},\n".format(string, str(tuple(df.iloc[i])))
    string = string[:-2] + ';'
    return string