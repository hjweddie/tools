from nginx import config


path = r'./default'
nc = config.Parser()
nc.loadf(path)
#take_effect_item_arr = [('upstream', 'http'), '#server']
#nc.toggle(take_effect_item_arr, "127.0.0.1:8001 weight=3")
#print "file content:", nc.gen_config()
print "data:", nc.data

#lose_effect_item_arr = [('upstream', 'http'), 'server']
#lose_effect_item_arr_test = [('server',), ('location', r'/doc/'), 'alias']
#print "--------------------------------------------------"
#toggle(path, take_effect_item_arr, "127.0.0.1:8001")
#print "--------------------------------------------------"
#toggle(path, lose_effect_item_arr, "127.0.0.1:8002")
#print "--------------------------------------------------"
#toggle(path, lose_effect_item_arr_test, "/usr/share/doc/")
#print "--------------------------------------------------"


class Block:
    def __init__(self):
        self._name = None
        self._value = None
        self._param = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, dest):
        self._name = dest

    @name.deleter
    def name(self):
        del self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, dest):
        self._name = dest

    @value.deleter
    def value(self):
        del self._value

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, dest):
        self._param = dest

    @param.deleter
    def param(self):
        del self._param


class Item:
    def __init__(self):
        self._name = None
        self._value = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, dest):
        self._name = dest

    @name.deleter
    def name(self):
        del self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, dest):
        self._name = dest

    @value.deleter
    def value(self):
        del self._value
