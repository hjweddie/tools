#
#  Author:   huangjunwei@youmi.net
#  Time:     Tue 20 Jan 2015 03:43:40 PM HKT
#  File:     init.py
#  Desc:
#

import yaml
from optparse import OptionParser
from fabric.api import env
from fabric.operations import prompt


def initialize():
    parser = OptionParser()
    parser.add_option("-c", "--config", type=str, dest="config", default="conf/setting.yml",  help="your configuration")

    (options, args) = parser.parse_args()

    fd = open(options.config, "r")
    data = yaml.load(fd)

    for key in data:
        env[key] = data[key]

    upstreams = {}
    for host in env.hosts:
        upstreams[host] = {}
        upstreams[host]["user"] = prompt("Please imput username of %s: " % (host))
        upstreams[host]["password"] = prompt("Please imput password of %s: " % (host))

    print upstreams
