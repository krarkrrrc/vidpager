import sys
sys.path = ['.', '..'] + sys.path
from bot import StoreSubtitlesFromUrlid
import ScanTools
from db import DbTools
import CONST
import os.path

"""
Main entry point for program
"""

#TODO validate sys.argv[1], only string and spaces should be allowed

if sys.argv[2] == None:
    test_urlid = CONST.test_urlids[0]
else:
    test_urlid = sys.argv[2]
    #check if input was whole url
    if len(test_urlid) > 11:
        test_urlid = test_urlid[-11:]
# make sure db exists, create one if not
if not ( os.path.isfile( './' + CONST.db_name ) ):
    DbTools.init()
    DbTools.insert(StoreSubtitlesFromUrlid.store(test_urlid))
else:
    try:
        DbTools.get_data(test_urlid, 'urlid') == test_urlid
        print(test_urlid, 'is already stored.\n')
        #video is already stored
        pass
    except TypeError:
        #save new video
        print('Saving subtitles for video',test_urlid,'\n')
        DbTools.insert(StoreSubtitlesFromUrlid.store(test_urlid))

# search vid for keyword provided from cmd line
for match in ScanTools.text_search( test_urlid, sys.argv[1] ):
    print( match['timestamp'] + ' - "' + match['caption'] + '"\n', match['url'] + '\n' )
