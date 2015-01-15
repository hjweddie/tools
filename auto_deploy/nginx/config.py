#!/usr/bin/env python
# encoding: utf-8

# block -> dict{ "name": "upstream", "param": "http", "value": [ block or items ] }
# item  -> tuple( "name", "value" )


class Config:
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

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __call__(self):
        return self.gen_config()

    # 获取节点值
    def get_value(self, data):
        if isinstance(data, tuple):
            return data[1]
        elif isinstance(data, dict):
            return data['value']
        else:
            return data

    # 获取节点名
    def get_name(self, data):
        if isinstance(data, tuple):
            return data[0]
        elif isinstance(data, dict):
            return data['name']
        else:
            return data

    # 设置节点
    # item_arr -> 节点路径
    # steps:
    #     1. get its parent
    #     2. set via its parent
    def set(self, item_arr, value=None, param=None, name=None):
        # 寻找父节点
        # 最外层item
        if isinstance(item_arr, str):
            elem = item_arr  # str
            parent = self.data
        # 最外层block
        elif isinstance(item_arr, list) and len(item_arr) == 1:
            elem = item_arr[0]  # tuple
            parent = self.data
        # 内层block或item
        else:
            elem = item_arr[-1]  # tuple
            parent = self.get_value(self.get(item_arr[0:-1]))

        if parent is None:
            raise KeyError('No such block.')

        # 通过父节点设置
        # 最外层item
        if isinstance(elem, str) and isinstance(value, str):
            # modifying text parameter
            for i, param in enumerate(parent):
                if isinstance(param, tuple):
                    if param[0] == elem:
                        if value is not None and name is not None:
                            parent[i] = (name, value)
                            return
                        elif value is not None:
                            parent[i] = (param[0], value)
                            return
                        elif name is not None:
                            parent[i] = (name, param[1])
                            return
                        raise TypeError('Not expected value type')

        elif isinstance(elem, tuple):
            # modifying block
            if len(elem) == 1:
                elem = (elem[0], '')
            for i, block in enumerate(parent):
                if isinstance(block, dict):
                    if elem == (block['name'], block['param']):
                        if value is not None and isinstance(value, list):
                            parent[i]['value'] = value
                            return
                        if param is not None and isinstance(param, str):
                            parent[i]['param'] = param
                            return
                        if name is not None and isinstance(name, str):
                            parent[i]['name'] = name
                            return
                        raise TypeError('Not expected value type')
        raise KeyError('No such parameter.')

    # 获取节点
    def get(self, item_arr, data=[]):
        if data == []:
            data = self.data
        # 外层block or item
        if type(item_arr) in [str, tuple]:
            item = item_arr
        # 外层block or 内层节点
        elif isinstance(item_arr, list):
            if len(item_arr) == 1:
                item = item_arr[0]
            else:
                element = item_arr[0]
                if isinstance(element, tuple):  # cannot be a string
                    # 只有name
                    if len(element) == 1:
                        element = (element[0], '')
                    for i, data_elem in enumerate(data):
                        if isinstance(data_elem, dict):
                            if element == (data_elem['name'], data_elem['param']):
                                return self.get(item_arr[1:], self.get_value(data[i]))

        if 'item' not in locals():
            raise KeyError('Error while getting parameter.')
        # 外层item
        if isinstance(item, str):
            for i, elem in enumerate(data):
                if isinstance(elem, tuple):
                    if elem[0] == item:
                        return data[i]
        # 外层item
        elif isinstance(item, tuple):
            if len(item) == 1:
                item = (item[0], '')
            for i, elem in enumerate(data):
                if isinstance(elem, dict):
                    if (elem['name'], elem['param']) == item:
                        return data[i]
        return None

    # 添加节点
    # position -> insert index
    def append(self, item, root=[], position=None):
        if root == []:
            root = self.data
        elif root is None:
            raise AttributeError('Root element is None')
        if position:
            root.insert(position, item)
        else:
            root.append(item)

    # 删除节点
    def remove(self, item_arr, data=[]):
        if data == []:
            data = self.data
        if type(item_arr) in [str, tuple]:
            item = item_arr
        elif isinstance(item_arr, list):
            if len(item_arr) == 1:
                item = item_arr[0]
            else:
                elem = item_arr.pop(0)
                if type(elem) in [tuple, str]:
                    self.remove(item_arr, self.get_value(self.get(elem, data)))
                    return

        if isinstance(item, str):
            for i, elem in enumerate(data):
                if isinstance(elem, tuple):
                    if elem[0] == item:
                        del data[i]
                        return
        elif isinstance(item, tuple):
            if len(item) == 1:
                item = (item[0], '')
            for i, elem in enumerate(data):
                if isinstance(elem, dict):
                    if (elem['name'], elem['param']) == item:
                        del data[i]
                        return
        else:
            raise AttributeError("Unknown item type '%s' in item_arr" % item.__class__.__name__)
        raise KeyError('Unable to remove')

    # 配置项开/关注释
    def toggle(self, item_arr, value):
        parent_id = item_arr[0:-1]
        parent = self.get(parent_id)
        parent_value = self.get_value(parent)
        new_value = []
        for row in parent_value:
            n = row[0]
            v = row[1]

            if v == value:
                if '#' == n[0]:
                    # to take effect
                    n = n[1:]
                else:
                    # to lose effect
                    n = "%s%s" % ('#', n)
            new_row = (n, v)
            new_value.append(new_row)
        self.set(parent_id, value=new_value)

    # 读取配置 - 字符串
    # 读取完成后进行配置解析
    def load(self, config):
        self.config = config
        self.length = len(config) - 1
        self.i = 0
        self.data = self.parse_block()

    # 读取配置 - 文件
    def loadf(self, filename):
        with open(filename, 'r') as f:
            conf = f.read()
            self.load(conf)

    # 生成新配置文件
    def savef(self, filename):
        try:
            f = open(filename, 'w')
            conf = self.gen_config()
            f.write(conf)
        finally:
            f.close()

    # 块解析器
    def parse_block(self):
        data = []
        param_name = None
        param_value = None
        buf = ''
        while self.i < self.length:
            # 换行符可能block换行或item之间的换行
            if self.config[self.i] == '\n':  # multiline value
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
                    #################################
                    buf += self.config[self.i]
                    #################################
                    # 使value变为list
                    # if param_value is None:
                    #    param_value = []

                    # if len(buf.strip()) > 0:
                    #    param_value.append(buf.strip())
                    #    buf = ''
            elif self.config[self.i] == ';':
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
            elif self.config[self.i] == '{':
                self.i += 1
                # tag
                block = self.parse_block()
                # tag
                data.append({'name': param_name, 'param': buf.strip(), 'value': block})
                param_name = None
                param_value = None
                buf = ''
            elif self.config[self.i] == '}':
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

    def gen_block(self, blocks, offset):
        subrez = ''  # ready to return string
        block_name = None
        block_param = ''
        for i, block in enumerate(blocks):
            if isinstance(block, tuple):
                if isinstance(block[1], str):
                    subrez += self.off_char * offset + '%s %s;\n' % (block[0], block[1])
                else:  # multiline
                    subrez += self.off_char * offset + '%s %s;\n' % (block[0], self.gen_block(block[1], offset + len(block[0]) + 1))

            elif isinstance(block, dict):
                block_value = self.gen_block(block['value'], offset + 4)
                if block['param']:
                    param = block['param'] + ' '
                else:
                    param = ''
                if subrez != '':
                    subrez += '\n'
                subrez += '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                    'offset': self.off_char * offset, 'name': block['name'], 'data': block_value,
                    'param': param}

            elif isinstance(block, str):  # multiline params
                if i == 0:
                    subrez += '%s\n' % block
                else:
                    subrez += '%s%s\n' % (self.off_char * offset, block)

        if block_name:
            return '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                'offset': self.off_char * offset, 'name': block_name, 'data': subrez,
                'param': block_param}
        else:
            return subrez

    def gen_config(self, offset_char=''):
        self.off_char = offset_char
        return self.gen_block(self.data, 0)
