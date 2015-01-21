#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Wed 21 Jan 2015 11:28:34 AM HKT
#  File:     supervisor/command.py
#  Desc:
#
from fabric.api import run, env, sudo


def _supervisorctl_command(command, process_name, bin=None, is_sudo=True):
    if bin is None:
        bin = env.supervisorctl_bin

    cmd = "%(bin)s %(command)s %(process_name)s" % locals()

    if is_sudo:
        sudo(cmd)
    else:
        run(cmd)


def supervisorctl_restart(process_name, bin=None, is_sudo=True):
    _supervisorctl_command("restart", process_name, bin=bin, is_sudo=is_sudo)


def supervisorctl_start(process_name, bin=None, is_sudo=True):
    _supervisorctl_command("start", process_name, bin=bin, is_sudo=is_sudo)


def supervisorctl_stop(process_name, bin=None, is_sudo=True):
    _supervisorctl_command("stop", process_name, bin=bin, is_sudo=is_sudo)


def _supervisord_command(command, bin=None, is_sudo=True):
    pass


def supervisord_restart(bin=None, is_sudo=True):
    pass


def supervisord_start(bin=None, is_sudo=True):
    pass


def supervisord_stop(bin=None, is_sudo=True):
    pass
