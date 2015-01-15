from nginx import config


def toggle(path, item_arr, value):
    nc = config.Config()
    nc.loadf(path)

    parent_id = item_arr[0:-1]
    parent = nc.get(parent_id)
    parent_value = nc.get_value(parent)
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
    nc.set(parent_id, value=new_value)
    print "lose effect result:\n", nc.gen_config()


path = r'./default'
nc = config.Config()
nc.loadf(path)
take_effect_item_arr = [('upstream', 'http'), '#server']
nc.toggle(take_effect_item_arr, "127.0.0.1:8001 weight=3")
print "file content:", nc.gen_config()
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
