import os
from parse import blast_parse
from flask import Flask, render_template, url_for, redirect, flash
from flask.globals import request
from werkzeug.utils import secure_filename
import blast_query
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

app = Flask(__name__)

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'fasta'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 5 * 1024 * 1024
app.secret_key = b'\x8b\xe7\x13\xd7L\xb5}\x199}\x1a\xdb'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query/', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            result = blast_query.run_query(UPLOAD_FOLDER+"/"+filename)
            if result:
                return redirect(url_for('results'))
            else:
               return render_template("error.html") 
        else:
            flash('No file part')
            return render_template("error.html")
    else:
        return render_template("query.html")

@app.route('/results/', methods=['GET', 'POST'])
def results():
    result = blast_parse("my_blast.xml")
    headers=["Description","Seq. Id.","Accession", "Acc. Length","E Value","Blast Score"]

    return render_template("results.html", headers=headers, content=result)

if __name__ == "__main__":
    app.run(debug=True)