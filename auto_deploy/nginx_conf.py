from python_nginx import pynginxconfig


def toggle(path, item_arr, value):
    nc = pynginxconfig.NginxConfig()
    nc.loadf(path)

    parent_id = item_arr[0:-1]
    print "parent_id:", parent_id
    parent = nc.get(parent_id)
    print "parent:", parent
    parent_value = nc.get_value(parent)
    print "parent_value:", parent_value
    # if isinstance(this, list):
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
        print "new_row:", new_row
        new_value.append(new_row)
    print "new_value:", new_value
    print "parent id:", parent_id
    nc.set(parent_id, value=new_value)
    # elif isinstance(parent, str):
    print "lose effect result:\n", nc.gen_config()


path = r'./default'
take_effect_item_arr = [('upstream', 'http'), '#server']
lose_effect_item_arr = [('upstream', 'http'), 'server']
lose_effect_item_arr_test = [('server',), ('location', r'/doc/'), 'alias']

print "--------------------------------------------------"
toggle(path, take_effect_item_arr, "127.0.0.1:8001")
print "--------------------------------------------------"
#toggle(path, lose_effect_item_arr, "127.0.0.1:8002")
print "--------------------------------------------------"
toggle(path, lose_effect_item_arr_test, "/usr/share/doc/")
print "--------------------------------------------------"
