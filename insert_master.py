#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torndb
import random
import md5
import time
# from multiprocessing import Pool

db = torndb.Connection("127.0.0.1:3306", "test", "root", "123")
#db = torndb.Connection("127.0.0.1:3308", "test", "root", "123")


def insert(times):
    ip = '.'.join('%s' % random.randint(0, 255) for _ in range(4))
    c = md5.new(ip).hexdigest()
    query = "REPLACE INTO `data` (`uk`, `c`) VALUES ('%s', '%s')" % (ip, c)

    for i in range(1, times):
        ip = '.'.join('%s' % random.randint(0, 255) for _ in range(4))
        c = md5.new(ip).hexdigest()
        query = "%s, ('%s', '%s')" % (query, ip, c)

    query = "%s;" % (query)
    # print query
    lastid = db.insert(query)
    print "lastid:", lastid

if "__main__" == __name__:
    for i in range(1, 1000):
        insert(900)
        if 0 == i % 20:
            time.sleep(1)
