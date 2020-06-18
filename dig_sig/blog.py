from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from dig_sig.auth import login_required
from dig_sig.db import get_db
from dig_sig.en_de import encrypt_image, decrypt_image
import os
from dig_sig.model import mode1_pred

# UPLOAD_FOLDER = "\uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#sub_obj = SubjectPred()
bp = Blueprint('blog', __name__)

@bp.route('/home')
def home():
    db = get_db()
    applicationdata = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM application_data p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/home.html', applicationdata=applicationdata)

@bp.route('/dashboard', methods=('GET', 'POST'))
def index():
    return render_template('blog/index.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        to=request.form['to']
        body = request.form['body']
        designation = request.form.get('desi', False)
        institute_name = request.form.get('insti')
        error = None
        subject = mode1_pred(body)
        print(subject)
        if not to:
            error='to is required'
       
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO application_data (title, body, author_id, subject)'
                ' VALUES (?, ?, ?,?)',
                (to, body, g.user['id'], subject)
            )
            db.commit()
            #return redirect(url_for('blog.subjectP'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, body, created, author_id, username, subject'
        ' FROM application_data p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        to = request.form['to']
        body = request.form['body']
        error = None

        if not to:
            error = 'to is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE application_data SET subject = ?'
                ' WHERE id = ?',
                (subject, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
@login_required
def view(id):
    post = get_post(id)
    if request.method =='POST':
        key=request.form['key']
        decrypt_image(key)
        flash("The signature has been validated")
    return render_template('blog/view.html', post=post)

@bp.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        print(os.getcwd())
        os.chdir("D:\\Dig_application\\uploads") 
        f.save(f.filename)
        os.chdir("D:/Dig_application") 
        key=encrypt_image("D:/Dig_application/uploads/signature.png")
        print("Encrypted the image")
        decrypt_image(key)
        print("Decrypted The image")
        return 'file uploaded successfully' 

@bp.route('/signatories',methods=('GET','POST'))
def signatories():
    return render_template('blog/signatories.html')

@bp.route('/signatories1',methods=('GET','POST'))
def signatories1():
    if request.method == 'POST':
        no_of_signatories=request.form['no_of_signatures']
        Name=request.form['Name']
        Designation = request.form['Designation']
        Institute = request.form['Institute']
        error = None
        if not to:
            error='to is required'
       
        if error is not None:
            flash(error)
        else:
            db = get_db()
            for i in range(no_of_signatures):
                db.execute(
                    'INSERT INTO signatories_table(sig_name, designation, institute_name)'
                    ' VALUES (?, ?, ?)',
                    (Name, Designation, Institute)
                )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/signatories1.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM application_data WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/',methods=('GET','POST'))
def about():
    return render_template('blog/about.html')

@bp.route('/home_sign',methods=('GET','POST'))
def home_sign():
    return render_template('blog/home_sign.html')

@bp.route('/index_sign',methods=('GET','POST'))
def index_sign():
    return render_template('blog/index_sign.html')


@bp.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    os.chdir("D:\\Dig_application\\uploads") 
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            url = image.save(image.filename)
            #print(url)
            key=encrypt_image("D:/Dig_application/uploads/signature.png")
            print("Image saved")
            print(key)

    return render_template("auth/login.html")

@bp.route('/<int:id>/subjectP', methods=('GET', 'POST'))
def subjectP(id):
    post = get_post(id)
    return render_template('blog/subject.html', post=post)
