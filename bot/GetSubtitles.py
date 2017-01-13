#!/usr/bin/env python
import sys
sys.path.append( '..' )
from db import vpdb
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

def get_subtitles(input_video):
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


#print(get_subtitles(get_yt_sub_url(test_ids[0])))

# cant find a working codec to decode the byte response
vpdb.insert( 'test-title', 'test-link', get_subtitles( get_yt_sub_url( test_ids[0] ) ).decode( 'utf8' ) )
