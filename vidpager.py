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

test_urlid = '3NxKH1MK4z8'
# make sure db exists, create one if not
if not ( os.path.isfile( './' + CONST.db_name ) ):
    DbTools.init()
    StoreSubtitlesFromUrlid.store( test_urlid )

# search vid for keyword provided from cmd line
for match in ScanTools.text_search( test_urlid, sys.argv[1] ):
    print( match['timestamp'] + ' - "' + match['caption'] + '"\n', match['url'] + '\n' )

