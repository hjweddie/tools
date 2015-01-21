#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Tue 20 Jan 2015 04:33:57 PM HKT
#  File:     main.py
#  Desc:
#

import init
import time
from fabric.api import env, sudo
#from nginx import command
from fs import operations
from pc import supervisor


if "__main__" == __name__:
    init.initialize()

    env.host_string = "172.16.1.250"
    env.user = "ymserver"

    now = time.strftime("%Y%m%d%H%M%S")
    dest_dir = "/home/ymserver/bin/feedback-server/bin/releases/sdk-fb"
    dest = "%s-%s" % (dest_dir, now)
    operations.upload("/home/eddie/workspace/gocode/src/feedback-server/bin/sdk-fb", dest, is_sudo=False, mode=0755)
    operations.ln(dest, "/home/ymserver/bin/feedback-server/bin/sdk-fb", is_sudo=False)
    supervisor.supervisorctl_restart("feedback_server")
