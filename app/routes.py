from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session, jsonify, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask import current_app
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
    EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
import logging
import sys
from app.program import mmm, test, test1
from time import sleep
import os
import spotipy
from MoveMyMusic.config import Default

caches_folder = './.spotify_caches/'
def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/usage',  methods=['GET', 'POST'])
@login_required
def usage():
    if request.method == 'POST':
        session['source'], session['target'] = request.form.getlist('myselect')
        session['sourceLogin'] = request.form.get('sourceLogin')
        session['sourcePassword'] = request.form.get('sourcePassword')
        session['targetLogin'] = request.form.get('targetLogin')
        session['targetPassword'] = request.form.get('targetPassword')
        session['user_config'] = request.form.getlist('mycheckbox')
        current_app.logger.debug(session)
        if session['source'] == '0':
            flash('Source cant be empty')
            current_app.logger.error('Source empty')

        if session['source'] == session['target']:
            flash('source and target cant be equal')
            current_app.logger.error('source == target')

        elif not (session['sourceLogin']):
            flash('Source credentials cant be empty')
            current_app.logger.error('Source credentials cant be empty')

        elif not session['sourcePassword'] and session['source'] != 'SP':
            flash('Source credentials cant be empty')
            current_app.logger.error('Source credentials cant be empty')

        elif session['target'] != '0' and (not session['targetLogin']):
            flash('Target credentials cant be empty')
            current_app.logger.error('Target credentials cant be empty')
        elif not session['user_config']:
            flash('Select config')
            current_app.logger.debug('CONFIG', session['user_config'])
        else:
            if session['source'] == 'SP':
                session['sourcePassword'] == '0'
            elif session['target'] == 'SP':
                session['targetPassword'] == '0'
            return redirect(url_for('confirm'))

    return render_template('usage.html', title='zaebal', button_state='disabled')



@app.route('/usage-confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=Default.SCOPE,
                                                show_dialog=True)



    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        flash('got token')
        return redirect(url_for('confirm'))

    if not auth_manager.get_cached_token():
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        # return f'<h2><a href="{auth_url}">Sign in</a></h2>'
        flash('no token')
        return redirect(auth_url)

    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template('confirm.html', title='Confirm run')


@app.route('/run', methods=['POST'])
@login_required
def run():
    resp = mmm(s=request.form['s'], s_user=request.form['s_user'], s_pass=request.form['s_pass'],
                 t=request.form['t'], t_user=request.form['t_user'], t_pass=request.form['t_pass'],
                 conf=request.form['conf'])
    return jsonify(resp)

@app.route('/features')
def features():
    form = LoginForm()
    return render_template('features.html', title='piza', form=form)


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        return render_template('index.html', title='sosi', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=True)
    return render_template('index.html', title='sosi', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
