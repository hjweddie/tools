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
