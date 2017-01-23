import datetime

epoch = datetime.datetime.utcfromtimestamp(0)
db_name = 'vidinfo.db'
caption_patt = '[\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+'
timestamp_patt = '\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d'
synctag_patt = '<\d+>'
vp_error = 'VIDPAGER ERROR: '
