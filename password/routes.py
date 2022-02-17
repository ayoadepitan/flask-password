from ast import Pass
import re
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from password import app, bcrypt, db
from password.forms import RegistrationForm, LoginForm, UpdateAccountForm, PasswordForm
from password.models import User, Password

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        passwords = Password.query.filter_by(owner=user).order_by(Password.name)
        return render_template('home.html', passwords=passwords, user=user)
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

def domain_name(website):
    url = re.compile(r"https?://(www\.)?")
    name = url.sub('', website).strip().strip('/')
    return name

@app.route("/password/new", methods=['GET', 'POST'])
@login_required
def new_password():
    form = PasswordForm()
    if form.validate_on_submit():
        password = Password(website=form.website.data, name=domain_name(form.website.data), email=form.email.data, username=form.username.data, password=form.password.data, owner=current_user)
        db.session.add(password)
        db.session.commit()
        flash('Your password has been saved!', 'success')
        return redirect(url_for('home'))
    return render_template('create_password.html', title='New Password', form=form, legend='New Password')

@app.route("/password/<int:password_id>")
def password(password_id):
    password = Password.query.get_or_404(password_id)
    return render_template('password.html', title=password.website, password=password)

@app.route("/password/<int:password_id>/update", methods=['GET', 'POST'])
@login_required
def update_password(password_id):
    password = Password.query.get_or_404(password_id)
    if password.owner != current_user:
        abort(403)
    form = PasswordForm()
    if form.validate_on_submit():
        password.website = form.website.data
        password.name = domain_name(form.website.data)
        password.email = form.email.data
        password.username = form.username.data
        password.password = form.password.data
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.website.data = password.website
        form.email.data = password.email
        form.username.data = password.username
        form.password.data = password.password
        
    return render_template('update_password.html', title='Update password', form=form, legend='Update password', password=password)

@app.route("/password/<int:password_id>/delete", methods=['POST'])
@login_required
def delete_password(password_id):
    password = Password.query.get_or_404(password_id)
    if password.owner != current_user:
        abort(403)
    db.session.delete(password)
    db.session.commit()
    flash('Your password has been deleted!', 'success')
    return redirect(url_for('home'))