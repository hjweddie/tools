from python_nginx import pynginxconfig


def toggle(path, item_arr, value):
    nc = pynginxconfig.NginxConfig()
    nc.loadf(path)

    this_name = item_arr[-1]

    parent_id = item_arr[0:-1]
    parent = nc.get(parent_id)
    parent_value = nc.get_value(parent)
    print "parent_value:", parent_value
    # if isinstance(this, list):
    new_value = []
    for row in parent_value:
        v = row[1]
        n = row[0]

        if v == value:
            if '#' == n[0]:
                # to take effect
                n = n[1:]
            else:
                # to lose effect
                n = "%s%s" % ('#', n)
                this_name = n
        new_row = (n, v)
        new_value.append(new_row)
    nc.set(parent_id, value=new_value, name=this_name)
    # elif isinstance(parent, str):
    print "lose effect result:\n", nc.gen_config()


path = r'/etc/nginx/sites-enabled/default'
take_effect_item_arr = [('upstream', 'http'), '#server']
lose_effect_item_arr = [('upstream', 'http'), 'server']
lose_effect_item_arr_test = [('server',), ('location', '/doc/'), 'alias']

#print "--------------------------------------------------"
#toggle(path, take_effect_item_arr, "127.0.0.1:8001")
#print "--------------------------------------------------"
#toggle(path, lose_effect_item_arr, "127.0.0.1:8002")
print "--------------------------------------------------"
toggle(path, lose_effect_item_arr_test, "/usr/share/doc/")
print "--------------------------------------------------"
