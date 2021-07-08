import MoveMyMusic
from flask import render_template, flash, redirect, url_for, request, session, jsonify, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from flask import current_app
from app import app
from app.forms import LoginForm, SourceForm, TargetForm
from app.models import User
from app.program import mmm, test, test1
import os
import spotipy
from MoveMyMusic.config import Default

caches_folder = './.spotify_caches/'


def session_cache_path():
    return caches_folder + session.get('uuid')


@app.route('/usage',  methods=['GET', 'POST'])
@login_required
def usage():
    # s_form = SourceForm()
    # t_form = TargetForm()
    # c_form = ConfirmForm()
    return render_template('usage.html', title='zaebal')



@app.route('/vk-login', methods=['POST'])
@login_required
def vkLogin():
    resp = {}
    vkaudio = MoveMyMusic.VK.get_auth(request.form['login'], request.form['pass'])
    if request.form['get_playlists']:
        resp['playlist_list'] = MoveMyMusic.VK.get_playlists(vkaudio)
    resp['success'] = 1

    return jsonify(resp)


@app.route('/ym-login', methods=['POST'])
@login_required
def ymLogin():
    resp = {}
    ym = MoveMyMusic.yandexmusic.YandexMusic(request.form['login'], request.form['pass'], export_data=None)
    ym.get_auth()
    session['ym_token'] = ym.client.token
    if request.form['get_playlists']:
        current_app.logger.warning('get_playlist TRUE')
        resp['playlist_list'] = ym.get_playlists()
    resp['success'] = 1

    return jsonify(resp)


@app.route('/sp-login', methods=['GET', 'POST'])
@login_required
def spLogin():
    sp_username = session.get('spUsername')
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=Default.SCOPE,
                                               show_dialog=True, username=sp_username)

    if request.args.get("code"):
        current_app.logger.warning('step3')
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        flash('got token')
        return redirect(url_for('usage'))
    else:
        return 'BAN'


@app.route('/sp-token', methods=['POST'])
@login_required
def spToken():
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=Default.SCOPE,
                                               show_dialog=True, username=request.form['login'])
    current_app.logger.warning(request.form['login'])
    resp = {}
    if auth_manager.get_cached_token():
        current_app.logger.warning('yes token')
        sp = MoveMyMusic.spotify.Spotify(username=request.form['login'], scope=Default.SCOPE, data=None)
        sp.get_auth()
        # session['sp'] = sp
        if request.form['get_playlists']:
            resp['playlist_list'] = sp.get_playlists()
        resp['token'] = 1
    else:
        session['spUsername'] = request.form['login']

        auth_url = auth_manager.get_authorize_url()
        current_app.logger.warning('no token')
        resp['token'] = 0
        resp['auth_url'] = auth_url

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
            flash('Invalid username or password', 'danger')
            current_app.logger.warning('FLASH ERROR')
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
