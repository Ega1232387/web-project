import sys

import requests
from flask import Flask, render_template, redirect, make_response, jsonify, request, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from requests import get

from data import db_session, jobs_api, users_api
from data.add_job import AddJobForm
from data.depart_form import AddDepartForm
from data.login_form import LoginForm
from data.users import User
from data.jobs import Jobs, Category
from data.departments import Department
from data.register import RegisterForm
import os
from werkzeug.utils import secure_filename


path = "/".join(os.path.abspath(__file__).split("\\")[:-1])
#print(path)
UPLOAD_FOLDER = 'uploads'
TEXTURE_EXTENSIONS = {'png'}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/mars_explorer.db")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    departments = {dep.id: dep.title for dep in db_sess.query(Department).all()}
    return render_template("index.html", jobs=jobs, names=names, departments=departments, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            department=form.department.data,
            email=form.email.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        f = add_form.file.data
        filename = secure_filename(f.filename)
        print(filename)
        jobs = Jobs(
            job=add_form.job.data,
            work_size=add_form.work_size.data,
            department=add_form.department.data,
            category=add_form.category.data,
            is_finished=add_form.is_finished.data,
            file_name= secure_filename(add_form.file.data.filename).split(".")[0],
            file_type = secure_filename(add_form.file.data.filename).split(".")[1]
        )
        print(path)
        f.save(os.path.join(UPLOAD_FOLDER, 'original', filename))
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавление Работы', form=add_form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == current_user.id) | (
                                                      current_user.id == 1)).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.department.data = jobs.department
            form.is_finished.data = jobs.is_finished
            form.category.data = jobs.category
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == current_user.id) | (
                                                      current_user.id == 1)).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.department = form.department.data
            jobs.is_finished = form.is_finished.data
            jobs.category = form.category.data
            f = form.file.data
            filename = jobs.file_name + "." + jobs.file_type
            f.save(os.path.join(UPLOAD_FOLDER, 'edited', filename))
            jobs.is_edited = 1
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html', title='Редактирование Работы', form=form)

@app.route('/download/<int:id>', methods=['GET', 'POST'])
@login_required
def download(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.department == current_user.department) | (
                                              current_user.id == 1)).first()
    if jobs:
        return send_from_directory(path, "/".join([UPLOAD_FOLDER, 'original', jobs.file_name + "." + jobs.file_type]))

@app.route('/download2/<int:id>', methods=['GET', 'POST'])
@login_required
def download2(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.department == current_user.department) | (
                                              current_user.id == 1)).first()
    if jobs:
        print("/".join([UPLOAD_FOLDER, 'upload', jobs.file_name + "." + jobs.file_type]))
        return send_from_directory(path, "/".join([UPLOAD_FOLDER, 'edited', jobs.file_name + "." + jobs.file_type]))

@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.team_leader == current_user.id) | (
                                                  current_user.id == 1)).first()

    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def depart():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("departments.html", departments=departments, names=names,
                           title='List of Departments')


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_edit(id):
    form = AddDepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                          current_user.id == 1)).first()
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                          current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_depart.html', title='Department Edit', form=form)


@app.route('/depart_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_delete(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).filter(Department.id == id,
                                              (Department.chief == current_user.id) | (
                                                      current_user.id == 1)).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    app.run()


if __name__ == '__main__':
    main()
