#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Fri 16 Jan 2015 05:23:13 PM HKT
#  File:     parser.py
#  Desc:
#


class Parser:
    # block -> dict{ "name": "upstream", "param": "http", "value": [ block or items ] }
    # item  -> tuple( "name", "value" )
    def __init__(self, offset_char=' '):
        # 解析过程下表指针
        self.i = 0
        # 文件内容
        self.config = ''
        # 文件内容长度
        self.length = 0

        # 结构化Nginx配置
        self.data = []

        # tab or whitespace ~
        self.off_char = offset_char

    def __call__(self):
        return self.gen_config()

    # 读取配置 - 字符串
    # 读取完成后进行配置解析
    def load(self, config):
        self.config = config
        self.length = len(config) - 1
        self.i = 0
        return self.parse_block()

    # 读取配置 - 文件
    def loadf(self, filename):
        conf = ''
        with open(filename, 'r') as f:
            conf = f.read()
        return self.load(conf)

    # 块解析器
    def parse_block(self):
        data = []
        param_name = None
        param_value = None
        buf = ''
        while self.i < self.length:
            # 换行符可能block换行或item之间的换行
            if '\n' == self.config[self.i]:  # multiline value
                if buf and param_name:
                    if param_value is None:
                        param_value = []
                    # tag value
                    param_value.append(buf.strip())
                    buf = ''
            elif self.config[self.i] == ' ':
                if not param_name and len(buf.strip()) > 0:
                    # tag name
                    param_name = buf.strip()
                    buf = ''
                # has param_name or len(buf.strip()) == 0
                else:
                    buf += self.config[self.i]
            elif ';' == self.config[self.i]:
                if isinstance(param_value, list):
                    # tag value
                    param_value.append(buf.strip())
                else:
                    # tag value
                    param_value = buf.strip()
                # tag
                data.append((param_name, param_value))
                param_name = None
                param_value = None
                buf = ''
            elif '{' == self.config[self.i]:
                self.i += 1
                # tag
                block = self.parse_block()
                # tag
                data.append({'name': param_name, 'param': buf.strip(), 'value': block})
                param_name = None
                param_value = None
                buf = ''
            elif '}' == self.config[self.i]:
                self.i += 1
                return data
            elif self.config[self.i] == '#':  # skip comments
                if self.config[self.i + 1] == ' ':
                    while self.i < self.length and self.config[self.i] != '\n':
                        self.i += 1
                else:
                    buf += self.config[self.i]
            else:
                buf += self.config[self.i]
            self.i += 1
        return data
