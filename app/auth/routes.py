from app.auth import auth
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app.utils.sample_todos import todos
from app.forms import LoginForm

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        print('form submitted')
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)
