from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from data.users import *
from werkzeug.utils import redirect
from data.jobs import Jobs
import jobs_api
from flask_restful import Api
from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.jobs import JobsForm
from api_dir import users_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# для списка объектов
api.add_resource(users_resources.UserListResource, '/api/v2/users')

# для одного объекта
api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')


def main():
    db_session.global_init("mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=5000, host='127.0.0.1', )


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.hashed_password, password)


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = []
    if current_user.is_authenticated:
        for job in session.query(Jobs).filter(
                Jobs.team_leader_id == current_user.id):  # | Jobs.collaborators.any(current_user.id)):
            jobs.append(job)
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            hashed_password=form.hashed_password.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_news():
    if not current_user.is_authenticated:
        return redirect('/')
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = Jobs()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('jobs.html',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/newjob', methods=['GET', 'POST'])
def newjob():
    if not current_user.is_authenticated:
        return redirect('/')
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        newjob = Jobs(
            team_leader_id=current_user.id,
            description=form.description.data,
            work_size=form.work_size.data,
            start_date=form.start_date.data,
            is_finished=form.is_finished.data,
        )
        colls = list(map(int, form.collaborators.data.split(',')))
        for col in colls:
            newjob.collaborators.append(col)
        session.add(newjob)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', title='Новая работа', form=form)


if __name__ == '__main__':
    main()
