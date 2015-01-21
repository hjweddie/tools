#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Tue 20 Jan 2015 04:33:57 PM HKT
#  File:     main.py
#  Desc:
#

import init
from fabric.api import env, sudo
#from nginx import command
#from fs import operations
from pc import supervisor


if "__main__" == __name__:
    init.initialize()

    env.host_string = "172.16.1.250"
    env.user = "ymserver"

    supervisor.supervisorctl_restart("feedback_server")

    #operations.download("/etc/nginx/sites-enabled/default", "/home/eddie/Downloads", is_sudo=True)
    #operations.upload("/home/eddie/Downloads/testfile", "/tmp/testfile", is_sudo=False)
    #operations.ln("/tmp/testfile", "/tmp/softlink", is_sudo=False)
    #for host in env.hosts:
        #env.host_string = host["domain"]
        #env.user = host["user"]
        #env.password = None

        #print env

        #sudo("uname -r")
        #sudo("ifconfig")
    #command.reload(is_sudo=True)
    #command.start(is_sudo=True)
    #command.stop(is_sudo=True)
