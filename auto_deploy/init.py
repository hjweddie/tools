#
#  Author:   huangjunwei@youmi.net
#  Time:     Tue 20 Jan 2015 03:43:40 PM HKT
#  File:     init.py
#  Desc:
#

import yaml
from optparse import OptionParser
from fabric.state import env


def initialize():
    parser = OptionParser()
    parser.add_option("-c", "--config", type=str, dest="config", default="conf/setting.yml",  help="your configuration")

    (options, args) = parser.parse_args()

    fd = open(options.config, "r")
    data = yaml.load(fd)

    for key in data:
        env[key] = data[key]
