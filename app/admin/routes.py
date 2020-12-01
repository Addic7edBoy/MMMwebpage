from functools import wraps
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUsernameForm,
    ChangePasswordForm,
    NewUserForm,
)
from app.models import User
from app.admin import admin


def permission_required():
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin():
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required()(f)


@admin.route('/index')
@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            name=form.name.data,
            role=form.role.data)
        user.set_password(user.password)
        db.session.add(user)
        db.session.commit()
        flash('User %s successfully created' % user.username, 'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    return render_template(
        'admin/registered_users.html', users=users)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)



@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.username, 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(
            user.username, user.role), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/change-password', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot change the password of your own account. Please ask another '
              'administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(user.password)
        db.session.add(user)
        db.session.commit()
        flash('Password for user {} successfully changed to {}.'.format(
                user.username, user.password), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/change-username', methods=['GET', 'POST'])
@login_required
@admin_required
def change_username(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot change username of your own account. Please ask another '
              'administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        flash('Username for user {} successfully changed to {}.'.format(
            user.username, user.username), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


