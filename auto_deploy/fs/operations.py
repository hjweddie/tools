#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Wed 21 Jan 2015 10:33:06 AM HKT
#  File:     fs/operations.py
#  Desc:
#
from fabric.operations import get, put, local
from fabric.api import run, sudo
from fabric.contrib import files, project


def _command(cmd, is_sudo=False, is_local=False):
    if is_local:
        local(cmd)
    else:
        if is_sudo:
            sudo(cmd)
        else:
            run(cmd)


def ln(src, dest, is_sudo=False, is_local=False):
    if files.is_link(dest, use_sudo=is_sudo):
        cmd = "ln -sf %s %s" % (src, dest)
        _command(cmd, is_sudo=is_sudo, is_local=is_local)


# 打包、解包
def pack():
    pass


def unpack():
    pass


def upload_dir(local_dir, remote_dir, is_sudo=False):
    project.upload_project(local_dir, remote_dir, use_sudo=is_sudo)


# only for file
def download(remote_path, local_path, is_sudo=False):
    get(local_path=local_path, remote_path=remote_path, use_sudo=is_sudo)


# only for file
def upload(local_path, remote_path, is_sudo=False, mode=0644):
    put(local_path=local_path, remote_path=remote_path, use_sudo=is_sudo, mode=mode)


def ensure_dir(dir, is_sudo=False):
    if not files.exists(dir, use_sudo=is_sudo):
        cmd = "mkdir -p %s" % (dir)
        _command(cmd, is_sudo=is_sudo)


def remove_dir(dir, is_sudo=False):
    if not files.exists(dir, use_sudo=is_sudo):
        cmd = "mkdir -p %s" % (dir)
        _command(cmd, is_sudo=is_sudo)


# 以下待完善
# 对文件内容某行进行注释及解注释
def comment(filename, regex, is_sudo=False, comment_char='#'):
    pass


def uncomment(filename, regex, is_sudo=False, comment_char='#'):
    files.uncomment(filename, regex, use_sudo=is_sudo, char=comment_char)
