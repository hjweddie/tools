#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Wed 21 Jan 2015 10:33:06 AM HKT
#  File:     fs/operations.py
#  Desc:
#


from fabric.operations import get, put
from fabric.api import run, sudo
from fabric.contrib import files


def _command(cmd, is_sudo=False):
    if is_sudo:
        sudo(cmd)
    else:
        run(cmd)


def ln(src, dest, is_sudo=False):
    if files.is_link(dest, use_sudo=is_sudo):
        cmd = "ln -sf %s %s" % (src, dest)
        _command(cmd, is_sudo=is_sudo)


def download(remote_path, local_path, is_sudo=False):
    get(local_path=local_path, remote_path=remote_path, use_sudo=is_sudo)


def upload(local_path, remote_path, is_sudo=False):
    put(local_path=local_path, remote_path=remote_path, use_sudo=is_sudo)


def ensure_dir(dir, is_sudo=False):
    if not files.exists(dir, use_sudo=is_sudo):
        cmd = "mkdir -p %s" % (dir)
        _command(cmd, is_sudo=is_sudo)


def remove_dir(dir, is_sudo=False):
    if not files.exists(dir, use_sudo=is_sudo):
        cmd = "mkdir -p %s" % (dir)
        _command(cmd, is_sudo=is_sudo)


# 以下待完善
def comment(filename, regex, is_sudo=False, comment_char='#'):
    pass


def uncomment(filename, regex, is_sudo=False, comment_char='#'):
    files.uncomment(filename, regex, use_sudo=is_sudo, char=comment_char)
