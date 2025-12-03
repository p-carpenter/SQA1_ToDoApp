from app.auth import auth
from app import db
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app.utils.forms import LoginForm
from app.utils.models import User
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
import sqlalchemy.orm as so

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.get_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for(login))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # to deterine if url is absolute or relative
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
