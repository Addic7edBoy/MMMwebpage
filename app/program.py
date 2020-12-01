# import MoveMyMusic as mmm
from spotipy.oauth2 import SpotifyOAuth
import sys
import spotipy
from MoveMyMusic.__main__ import main
import logging
from flask import current_app
from time import sleep



def mmm(s, s_user, s_pass, t, t_user, t_pass, conf):
    sys_args = ['run', '--source', s.lower(), '--source-user',
                s_user, '--source-pass', s_pass, '--target', t.lower(), '--target-user', t_user, '--target-pass', t_pass]
    conf = eval(conf)
    for item in conf:
        sys_args.append(item)
    stat = main(sys_args)
    return stat



def test(s, s_user, s_pass, t, t_user, t_pass, conf):
    # current_app.logger.debug([s, s_user, s_pass, t, t_user, t_pass, conf])
    sleep(3)
    return 'WOW'


def test1(s, s_user, s_pass, t, t_user, t_pass, conf):
    sys_args = ['run', '--source', s, '--source-user',
                s_user, '--source-pass', s_pass, '--target', t, '--target-user', t_user, '--target-pass', t_pass]
    current_app.logger.debug(type(conf))
    conf = eval(conf)
    current_app.logger.debug(type(conf))
    for item in conf:
        sys_args.append(item)

    sleep(4)
    return sys_args



