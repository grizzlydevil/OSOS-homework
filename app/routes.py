from decathlon import export_file_to_json

from flask import render_template, redirect

from app import app
from app.forms import ImportFileForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImportFileForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data

        export_file_to_json(uploaded_file, 'flaskFile.json')

        return redirect('/')

    return render_template('index.html', form=form)
