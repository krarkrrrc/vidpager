import datetime
#aa
epoch = datetime.datetime.utcfromtimestamp(0)
db_name = 'vidinfo.db'
caption_patt = '[\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+'
timestamp_patt = '\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d'
raw_subs_patt = r'(\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d)\\n([\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+)\\n\\n'
asr_raw_subs_patt = r'(\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d)\n([\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+)\n'
synctag_patt = '<\d+>'
vp_error = 'VIDPAGER ERROR: '
youtube_data_api_key = 'AIzaSyCka9i9ib-4D698ZUQ5zgQYhE5gbstAfMA'

test_urlids = [
'3NxKH1MK4z8', #Great War week 129 - regular subtitles, multilang
'BTsgWepH3GY', #The Legend of Zelda: Twilight Princess'' dungeon design, no subtitles
'dFccny3iGbo', #Geography Now! Comoros - eng subtitles
'f_4Q9Iv7_Ao'  #Why sugar is bad
]

#ask_youtube_dl_for_asr_subtitles works here
test_urlids_for_asr = [
'ny1JpexzPUg' #What is the Strongest Daedric Artifact in the Elder Scrolls?
]
