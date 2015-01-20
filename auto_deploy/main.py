#
#  Author:   huangjunwei@youmi.net
#  Time:     Tue 20 Jan 2015 04:33:57 PM HKT
#  File:     main.py
#  Desc:
#

import init
from fabric.api import env
from nginx import command


if "__main__" == __name__:
    init.initialize()
    print env
    command.reload(is_sudo=True)
    #command.start(is_sudo=True)
    #command.stop(is_sudo=True)
