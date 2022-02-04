import csv

from flask import flash, render_template, redirect

from app import app
from app.forms import ImportFileForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImportFileForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data

        return redirect('/')

    return render_template('index.html', form=form)
