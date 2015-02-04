#!/usr/bin/env python
# encoding: utf-8
#
#  Author:   huangjunwei@youmi.net
#  Time:     Fri 16 Jan 2015 05:21:25 PM HKT
#  File:     nginx/config.py
#  Desc:
#

from parser import Parser
import re


class Config:
    # data 是配置文件路径或 数组
    def __init__(self, data):
        if type(data) is str:
            # if data is a file path
            self._data = Parser().loadf(data)
        else:
            # if data is raw data
            self._data = data
        self._position = []
        print self._data

    # 获取节点
    def _get(self, item_arr, data=[]):
        if [] == item_arr:
            return []

        if [] == data:
            data = self._data

        # 外层block or item
        if type(item_arr) in [str, tuple]:
            item = item_arr
        # 外层block or 内层节点
        if isinstance(item_arr, list):
            if 1 == len(item_arr):
                item = item_arr[0]
            else:
                element = item_arr[0]
                if isinstance(element, tuple):  # cannot be a string
                    # 只有name
                    if 1 == len(element):
                        element = (element[0], '')
                    for data_elem in data:
                        if 'block' == data_elem['type']:
                            if (data_elem['name'], data_elem['param']) == element:
                                return self._get(item_arr[1:], self._get_value(data_elem))
        else:
            item = item_arr

        if isinstance(item, str):
            for elem in data:
                if item == elem['name']:
                    return elem

        elif isinstance(item, tuple):
            if 1 == len(item):
                item = (item[0], '')
            for elem in data:
                if 'block' == elem['type'] and item[0] == elem['name'] and item[1] == elem['param']:
                    return elem

        return None

    # 获取节点值
    def _get_value(self, data):
        return data['value']

    # 获取节点名
    def _get_name(self, data):
        return data['name']

    # 设置节点
    # item_arr -> 节点路径
    # steps:
    #     1. get its parent
    #     2. set via its parent
    def _set(self, item_arr, value=None, param=None, name=None):
        # 寻找父节点
        if 1 == len(item_arr):
            parent = self._data
        else:
            parent = self._get_value(self._get(item_arr[0:-1]))

        elem = item_arr[-1]

        if parent is None:
            raise KeyError('No such block.')

        # 修改item
        if isinstance(elem, str):
            for i, child in enumerate(parent):
                if 'item' == child['type']:
                    if value is not None and isinstance(value, str):
                        child['value'] = value
                    if name is not None:
                        child['name'] = name

        elif isinstance(elem, tuple):
            # modifying block
            for i, child in enumerate(parent):
                if 'block' == child['type']:
                    if elem == (child['name'], child['param']):
                        if value is not None and isinstance(value, list):
                            parent[i]['value'] = value
                        if param is not None and isinstance(param, str):
                            parent[i]['param'] = param
                        if name is not None and isinstance(name, str):
                            parent[i]['name'] = name

    # 添加节点
    # position -> insert index
    def _append(self, item, root=[], position=None):
        if [] == root:
            root = self._data
        elif root is None:
            raise AttributeError('Root element is None')
        if position:
            root.insert(position, item)
        else:
            root.append(item)

    # 删除节点,仅限配置项
    def _remove(self, name, reg, root=[]):
        if [] == root:
            root = self._data
        elif root is None:
            raise AttributeError('Root element is None')

        for i, item in enumerate(root):
            if 'item' == item['type'] and re.search(reg, item['value']):
                del(root[i])

    def _parent(self, item_arr=[]):
        if [] == item_arr:
            if [] == self._position:
                return []
            else:
                return self._get(self._position[0:-1])
        else:
            return self._get(item_arr[0:-1])

    # 配置项开/关注释
    def _toggle(self, item_arr, reg):
        parent_id = item_arr[0:-1]
        this_name = item_arr[-1]
        parent = self._get(parent_id)
        parent_value = self._get_value(parent)
        new_value = []

        for child in parent_value:
            if 'item' == child['type']:
                n = child['name']
                v = child['value']

                if this_name in n and re.search(reg, v):
                    if '#' == n[0]:
                        # to take effect
                        n = n[1:]
                    else:
                        # to lose effect
                        n = "%s%s" % ('#', n)
                new_row = {'name': n, 'value': v, 'type': 'item'}
                new_value.append(new_row)
            else:
                new_value.append(child)
        self._set(parent_id, value=new_value)

    def gen_block(self, blocks, offset):
        subrez = ''
        block_name = None
        block_param = ''
        for i, block in enumerate(blocks):
            if 'item' == block['type']:
                if isinstance(block['value'], str):
                    subrez += self.off_char * offset + '%s %s;\n' % (block['name'], block['value'])
                else:
                    # multiline
                    subrez += self.off_char * offset + '%s %s;\n' % (block['name'], self.gen_block(block['value'], offset + len(block['name']) + 1))

            elif 'block' == block['type']:
                block_value = self.gen_block(block['value'], offset + 4)
                if block['param']:
                    param = block['param'] + ' '
                else:
                    param = ''
                if '' != subrez:
                    subrez += '\n'
                subrez += '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                    'offset': self.off_char * offset, 'name': block['name'], 'data': block_value,
                    'param': param}

            elif isinstance(block, str):
                # multiline params
                if 0 == i:
                    subrez += '%s\n' % block
                else:
                    subrez += '%s%s\n' % (self.off_char * offset, block)

        if block_name:
            return '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                'offset': self.off_char * offset, 'name': block_name, 'data': subrez,
                'param': block_param}
        else:
            return subrez

    ########################################################
    #                  可供外部访问的函数                  #
    ########################################################
    def gen_config(self, offset_char=' '):
        self.off_char = offset_char
        print "in gen_config:", self._data
        return self.gen_block(self._data, 0)

    # 生成新配置文件
    def savef(self, filename):
        with open(filename, 'w') as f:
            conf = self.gen_config()
            f.write(conf)

    @property
    def data(self):
        return self._data

    @property
    def position(self):
        return self._position

    # active record begin #

    # _get 的进化版，支持模糊搜索，返回符合条件的数组
    # def _vague_get(selfi, item_arr):
        # pass

    # 根据name查找
    # find('http', 'server', ('location', '/'))
    # condition allow str or tuple
    def find(self, *conditions):
        # 构造 _get 查询条件
        item_arr = []
        end = len(conditions) - 1
        for index, condition in enumerate(conditions):
            if type(condition) is tuple:
                item_arr.append(condition)
            elif type(condition) is str and index == end:
                item_arr.append((condition, ))
            else:
                item_arr.append((condition, ))

        self._position = self._position[0:-1] + item_arr

        return self

    # 根据值查找
    def where(self, name, reg):
        pass

    # 只能插入配置项
    def append(self, name, value, index=None):
        root = self._get_value(self._get(self._position))
        item = (name, value)
        self._append(item, root, index)
        return self

    def remove(self, name, reg='.*'):
        root = self._get_value(self._get(self._position))
        self._remove(name, reg, root)
        return self

    def parent(self):
        pass

    def toggle(self, name, reg='.*'):
        item_arr = [p for p in self._position]
        item_arr.append(name)
        self._toggle(item_arr, reg)
        return self

    # active record end   #

if __name__ == "__main__":
    path = r'./default'
    config = Config(path)

    print config.find(('upstream', 'http')).toggle('server', '8000').gen_config()
    # print config.find('http', 'server').append("addtional", "string").remove("additional", "string").gen_config()
    # config.savef(r'../default.result')
