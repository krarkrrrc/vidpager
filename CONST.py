import datetime

epoch = datetime.datetime.utcfromtimestamp(0)
db_name = 'vidinfo.db'
caption_patt = r'[\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\\"\-]+'
timestamp_patt = r'\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d'
raw_subs_patt = r'(\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d).*\n([\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+)\n\n'
synctag_patt = '<\d+>'
vp_error = 'VIDPAGER ERROR: '
youtube_data_api_key = 'AIzaSyCka9i9ib-4D698ZUQ5zgQYhE5gbstAfMA'
