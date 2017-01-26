import datetime

epoch = datetime.datetime.utcfromtimestamp(0) #where is this used?
db_name = 'vidinfo.db'
caption_patt = '[\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+'
timestamp_patt = '\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d'
synctag_patt = '<\d+>'
vp_error = 'VIDPAGER ERROR: '
youtube_data_api_key = 'AIzaSyCka9i9ib-4D698ZUQ5zgQYhE5gbstAfMA'

test_urlids = [
'3NxKH1MK4z8', #Great War week 129 - regular subtitles, multilang
'BTsgWepH3GY', #The Legend of Zelda: Twilight Princess'' dungeon design, no subtitles
'dFccny3iGbo' #Geography Now! Comoros - eng subtitles
]
