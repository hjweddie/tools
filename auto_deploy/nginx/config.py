#!/usr/bin/env python
# encoding: utf-8

from parser import Parser


class Config:
    # data 是配置文件路径或 数组
    def __init__(self, data):
        if type(data) is str:
            self._data = Parser().loadf(data)
        else:
            self._data = data
        self._position = []

    # 获取节点
    def _get(self, item_arr, data=[]):
        if [] == item_arr:
            return []

        if data == []:
            data = self._data
        # 外层block or item
        if type(item_arr) in [str, tuple]:
            item = item_arr
        # 外层block or 内层节点
        elif isinstance(item_arr, list):
            if 1 == len(item_arr):
                item = item_arr[0]
            else:
                element = item_arr[0]
                if isinstance(element, tuple):  # cannot be a string
                    # 只有name
                    if 1 == len(element):
                        element = (element[0], '')
                    for data_elem in data:
                        if isinstance(data_elem, dict):
                            if (data_elem['name'], data_elem['param']) == element:
                                return self._get(item_arr[1:], self._get_value(data_elem))

        if 'item' not in locals():
            raise KeyError('Error while getting parameter.')

        if isinstance(item, str):
            for elem in data:
                if isinstance(elem, tuple):
                    if elem[0] == item:
                        return elem
                #####################################
                if isinstance(elem, dict):
                    if elem['name'] == item:
                        return elem
                #####################################

        elif isinstance(item, tuple):
            if 1 == len(item):
                item = (item[0], '')
            for elem in data:
                if isinstance(elem, dict):
                    if (elem['name'], elem['param']) == item:
                        return elem

        return None

    # 获取节点值
    def _get_value(self, data):
        if isinstance(data, tuple):
            return data[1]
        elif isinstance(data, dict):
            return data['value']
        else:
            return data

    # 获取节点名
    def _get_name(self, data):
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
    def _set(self, item_arr, value=None, param=None, name=None):
        # 寻找父节点
        # 最外层item
        if isinstance(item_arr, str):
            elem = item_arr  # str
            parent = self._data
        # 最外层block
        elif isinstance(item_arr, list) and len(item_arr) == 1:
            elem = item_arr[0]  # tuple
            parent = self._data
        # 内层block或item
        else:
            elem = item_arr[-1]  # tuple
            parent = self._get_value(self._get(item_arr[0:-1]))

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
            if 1 == len(elem):
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

    # 删除节点(所有)
    def _remove(self, item_arr, data=[]):
        if [] == data:
            data = self._data
        if type(item_arr) in [str, tuple]:
            item = item_arr
        elif isinstance(item_arr, list):
            if 1 == len(item_arr):
                item = item_arr[0]
            else:
                elem = item_arr[0]
                if type(elem) in [tuple, str]:
                    self._remove(item_arr[1:], self._get_value(self._get(elem, data)))
                    return

        if isinstance(item, str):
            for i, elem in enumerate(data):
                if isinstance(elem, tuple):
                    if elem[0] == item:
                        del data[i]
                        return
        elif isinstance(item, tuple):
            if 1 == len(item):
                item = (item[0], '')
            for i, elem in enumerate(data):
                if isinstance(elem, dict):
                    if (elem['name'], elem['param']) == item:
                        del data[i]
                        return
        else:
            raise AttributeError("Unknown item type '%s' in item_arr" % item.__class__.__name__)
        raise KeyError('Unable to remove')

    def _parent(self, item_arr=[]):
        if [] == item_arr:
            if [] == self._position:
                return []
            else:
                return self._get(self._position[0:-1])
        else:
            return self._get(item_arr[0:-1])

    # 配置项开/关注释
    def _toggle(self, item_arr, value):
        parent_id = item_arr[0:-1]
        parent = self._get(parent_id)
        parent_value = self._get_value(parent)
        new_value = []
        for row in parent_value:
            n = row[0]
            v = row[1]

            # if v == value:
            if value in v:
                if '#' == n[0]:
                    # to take effect
                    n = n[1:]
                else:
                    # to lose effect
                    n = "%s%s" % ('#', n)
            new_row = (n, v)
            new_value.append(new_row)
        self._set(parent_id, value=new_value)

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
                if '' != subrez:
                    subrez += '\n'
                subrez += '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                    'offset': self.off_char * offset, 'name': block['name'], 'data': block_value,
                    'param': param}

            elif isinstance(block, str):  # multiline params
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
        return self.gen_block(self._data, 0)

    # 生成新配置文件
    def savef(self, filename):
        with open(filename, 'w') as f:
            conf = self.gen_config()
            f.write(conf)

    # toggle = _toggle
    get = _get

    @property
    def data(self):
        return self._data

    @property
    def position(self):
        return self._position

    # active record begin #

    # _get 的进化版，支持模糊搜索，返回符合条件的数组
    def _vague_get(selfi, item_arr):
        pass

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
                item_arr.append(condition)
            else:
                item_arr.append((condition, ))

        self._position = item_arr

        # 查找符合的所有节点，返回数组
        nodes = []
        this = self._get(self._position)
        parent = self._parent()
        if [] == parent:
            nodes.append(this)
        else:
            print "parent:", parent
            for child in parent["value"]:
                if (type(child), type(this)) == (dict, dict):
                    if child["name"] == this["name"] and child["param"] == child["param"]:
                        nodes.append(child)
                elif (type(child), type(this)) == (tuple, tuple):
                    if child[0] == this[0]:
                        nodes.append(child)

        return Config(nodes)

    def where(self):
        pass

    def remove(self):
        pass

    def parent(self):
        pass

    def toggle(self, item_arr, value):
        self._toggle(item_arr, value)

    # active record end   #

if __name__ == "__main__":
    path = r'../default'
    config = Config(path)
    #print "data:", config.data
    print "--------------------------------------------------"
    #lose_effect_item_arr = [('upstream', 'http'), 'server']
    locations = config.find('http', 'server', 'location')
    #print "location data:", locations.data
    #servers = item_arr = config.find(('upstream', 'http'), 'server')
    print "--------------------------------------------------"
    print locations.find(('location', '/doc/')).data

    #print config.get(item_arr)
    #lose_effect_item_arr_test = [('server',), ('location', r'/doc/'), 'alias']
    #print "--------------------------------------------------"
    #toggle(path, take_effect_item_arr, "127.0.0.1:8001")
    #print "--------------------------------------------------"
    #config.toggle(path, lose_effect_item_arr, "127.0.0.1:8002")
    #config.toggle(lose_effect_item_arr, "127.0.0.1:8002 weight=3")
    #config.toggle(lose_effect_item_arr, "weight=3")
    #print "data:", config.data

    #print "--------------------------------------------------"
    #toggle(path, lose_effect_item_arr_test, "/usr/share/doc/")
    #print "--------------------------------------------------"
    # print "data:", parser.data
