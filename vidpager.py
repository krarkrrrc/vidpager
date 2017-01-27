import CONST
import sys #for args
sys.path = ['.', '..'] + sys.path #what is this for?
from bot import StoreSubtitlesFromUrlid #for getting yt data
import ScanTools #for searching
from db import DbTools #for Db stuff
import os.path #for checking if db exist

"""
Main entry point for program
"""
#TODO validate sys.argv[1], only string and spaces should be allowed
#TODO when you get sober, sort all those tries lol

# make sure db exists, create one if not
if not ( os.path.isfile( './' + CONST.db_name ) ):
    DbTools.init()

#check if url is passed
try:
    input_url = sys.argv[2]
    #check if input was whole url, get only last 11 characters
    if len(input_url) > 11:
        input_url = input_url[-11:]
        #TODO url might be in middle of the link, use re
except IndexError:
    #no url passed, just search in whole db
    DbTools.search_all(sys.argv[1])

try:
    input_url
except NameError:
    pass
else:
    try:
        DbTools.get_data(input_url, 'urlid') == input_url
        print(input_url, 'is already stored.\n')
        #video is already stored
        pass
    except TypeError:
        #save new video
        print('Saving subtitles for video',input_url,'\n')
        DbTools.insert(StoreSubtitlesFromUrlid.store(input_url))

    # search vid for keyword provided from cmd line
    for match in ScanTools.text_search( input_url, sys.argv[1] ):
        print( match['timestamp'] + ' - "' + match['caption'] + '"\n', match['url'] + '\n' )
