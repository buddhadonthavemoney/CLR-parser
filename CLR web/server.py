
from curses.ascii import isupper
from typing import Type
import os
import collections
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
import os

from Parser.clr import main
from Parser.firstfollow import production_list, nt_list as ntl, t_list as tl
from Parser.clr import nt_list, t_list
app = Flask(__name__)
# LOGO = os.path.join('static', 'Group_1.png')
# app.config['UPLOAD_FOLDER'] = LOGO

# app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def hello_world():
    string = 'asdf'

    if request.method == 'POST':
        isError = False
        # for element in dir():
        #     if element[0:2] != "__":
        #         del globals()[element]
        # string = 'asdf'
        grammar = request.form['grammar']
        string = grammar.replace("\r", "").split("\n")
        to_parse = request.form['string']
        # string.append('')
        results = collections.Counter(grammar)
        head = list()
        ntList = list()
        gramList = grammar.split()
        print(gramList)
        if not all('->' in x for x in gramList):
            print('production error')
            isError = True
        else:
            ctr = 1
            gramLen = results['>']

            for i in range(gramLen):
                head, body = gramList[ctr-1].split('->')
                ntList.append(head)
                ctr += 1
            print(ntList)
            print(ctr)
            if not all(x.isupper() for x in ntList):
                print('grammar error')
                isError = True
            # raise TypeError('error')

        print(f'errors status is {isError}s')
        if isError:
            print('prod grammar error')
            return render_template('cannonical.html', hello="world", isError=isError)
        else:
            global production_list, tl, ntl, nt_list, t_list, first_list, follow_list

            items, sym_list, clr_items, goto_list, first_list, follow_list, input_test, string_validity, conflict = main(
                grammars=string, Input=to_parse)
            print(f'grammar {grammar}')
            print(f'variables {dir()}')
            return render_template('cannonical.html',
                                   dictionary=items,
                                   clr_items=clr_items,
                                   symbols=sym_list,
                                   goto_list=goto_list,
                                   first_list=first_list,
                                   follow_list=follow_list,
                                   input_test=input_test,
                                   grammar=grammar,
                                   input_string=to_parse,
                                   string_validity=string_validity,
                                   conflict=conflict
                                   )

    return render_template('cannonical.html', hello="world")
