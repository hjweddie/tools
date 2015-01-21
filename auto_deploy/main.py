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
from nginx import command, config
from fs import operations
from pc import supervisor


def feedback_server():
    init.initialize()

    env.host_string = "172.16.1.250"
    env.user = "ymserver"

    now = time.strftime("%Y%m%d%H%M%S")
    dest_dir = "/home/ymserver/bin/feedback-server/bin/releases/sdk-fb"
    dest = "%s-%s" % (dest_dir, now)
    operations.upload("/home/eddie/workspace/gocode/src/feedback-server/bin/sdk-fb", dest, is_sudo=False, mode=0755)
    operations.ln(dest, "/home/ymserver/bin/feedback-server/bin/sdk-fb", is_sudo=False)
    supervisor.supervisorctl_restart("feedback_server")


# 复杂部署过程v1.0, 待完善
def demos():
    ports = [8900, 8901, 8902, 8903]

    # download nginx config
    env.host_string = env.ba_host
    nginx_config_local_dest = "/tmp/fxcb.conf"
    nginx_config_local_tmp_dest = "/tmp/fxcb.conf.tmp"
    operations.download(env.nginx_config, nginx_config_local_dest)

    # to deploy on each upstream
    for upstream in env.upstream_hosts:
        # upload code to upstream
        env.host_string = upstream["server"]
        env.user = upstream["user"]
        env.passwprd = None
        operations.upload_dir(env.local_project_dir, env.remote_project_dir)

        for port in ports:
            nginx_config = config.Config(nginx_config_local_dest)
            tag = "%s:%s" % (upstream["server"], port)
            nginx_config.find(('upstream', env.upstream_block)).toggle('server', tag)
            nginx_config.savef(nginx_config_local_tmp_dest)

            # upload nginx config to ba_host
            print "disabling one line of upstream:", tag

            env.host_string = env.ba_host["server"]
            env.user = env.ba_host["user"]
            env.password = None
            operations.upload(nginx_config_local_tmp_dest, env.nginx_config)

            # sudo nginx -s reload
            command.reload()

            # restart process in supervisor
            env.host_string = upstream["server"]
            env.user = upstream["user"]
            env.password = None
            process_name = "fxcallback:fxcallback-%s" % port

            # sudo supervisorctl restart process_name
            supervisor.supervisorctl_restart(process_name)

            print "enabling one line of upstream:", tag
            env.host_string = env.ba_host["server"]
            env.user = env.ba_host["user"]
            env.password = None
            operations.upload(nginx_config_local_dest, env.nginx_config)

            # sudo nginx -s reload
            command.reload()


if "__main__" == __name__:
    feedback_server()
