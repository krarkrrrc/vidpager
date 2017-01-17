#!/usr/bin/env python
import sys
sys.path = ['.', '..'] + sys.path
import re
from db import DbTools
import urllib.request

"""
V0.1 GET yt subtitles
example API url to get subtitles
https://www.youtube.com/api/timedtext?lang=en&v=3NxKH1MK4z8&fmt=vtt&name=
"""

test_ids = [
'3NxKH1MK4z8' #Great War week 129
]

def get_yt_sub_url(id):
    """
    return API url
    TODO add format option
    """
    url = 'https://www.youtube.com/api/timedtext?lang=en&v=' + id +'&fmt=vtt&name='
    return url

def get_raw_subtitles(input_video):
    """
    return data of url
    TODO better return
    """
    try:
        get = urllib.request.urlopen(input_video)
        data = get.read()
        if len(data) > 0:
            return data
        else:
            return False # no subtitles
    except ValueError:
        print('Unkown url',input_video)

def get_title( url_or_urlid ):
    """
    returns title from url or urlid
    """
    return ""


def store( url_or_urlid ):
    """
    store a videos subtitles by either a urlid or url (not yet implement)
    TODO write url_validate code
    """
    url_validate_test = False
    urlid_validate_test = re.search( '[\d\w]{11}', url_or_urlid )
    if ( url_validate_test ):
        pass
    elif ( urlid_validate_test ):
        DbTools.insert_raw_subtitles( url_or_urlid, get_raw_subtitles( get_yt_sub_url( url_or_urlid ) ), get_title( url_or_urlid ) ) 
    else:
        raise ValueError( "Failed to store '" + url_or_urlid + "': did not validate" ) 
        

#subtitles =  str( get_subtitles( get_yt_sub_url( test_ids[0] ) ) )[2:-1]
#parsed_subs = parse_raw_subtitles( subtitles ) 
#DbTools.insert( 'test-title', 'test-urlid', parsed_subs['captions'], parsed_subs['timestamps'], '0') 

