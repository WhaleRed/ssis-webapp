from . import user_bp

from flask import render_template, redirect, request, jsonify, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import user_bp
from MyCollege.controllers.user.forms import LoginForm
from MyCollege.models.models import Users

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.login'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.username.data)
        print(form.password.data)
        user = Users.get_by_username(form.username.data)
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('general.colleges')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form, title='Login')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))