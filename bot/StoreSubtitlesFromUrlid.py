#!/usr/bin/env python
import sys
sys.path = ['.', '..'] + sys.path
import CONST
import re #for def store()
from db import DbTools #for def store()
from urllib.request import urlopen #to get subtitles
from pafy import new #for getting metadata
import datetime

"""
V0.1 GET yt subtitles
V0.2 GET video metadata using pafy
example API url to get subtitles
https://www.youtube.com/api/timedtext?lang=en&v=3NxKH1MK4z8&fmt=vtt&name=
"""

test_ids = [
'3NxKH1MK4z8' #Great War week 129 - regular subtitles, multilang
]

def get_yt_sub_url(id):
    """return yt API url to download subtitles in vtt format"""
    url = 'https://www.youtube.com/api/timedtext?lang=en&v=' + id +'&fmt=vtt&name='
    return url

def get_raw_subtitles(input_video):
    """
    return data from input_video url
    TODO better error handling
    """
    try:
        get = urlopen(input_video)
        data = get.read()
        if len(data) > 0:
            return data
        else:
            return False # no subtitles
    except ValueError:
        print('Unkown url',input_video)
        # TODO return error

def get_metadata(video_id):
    try:
        url = 'https://www.youtube.com/watch?v=' + video_id
        return new(url)
    except ValueError:
        print('Unkown url',url)
        # TODO return error


def get_title(video):
    return video.title
def get_author(video):
    return video.author
def get_length(video):
    #TODO must be str because of args_str = "','".join( args ) in DbTools.insert_args
    return str(video.length)
def get_date(video):
    date_str = video.published
    # verify date is valid
    try:
        DbTools.parse_date( date_str )
    except TypeError as e:
        print( CONST.vp_error + 'invalid date found for title: ' + video.title )
    return date_str
def get_category(video):
    return video.category
def get_tags(video):
    return ','.join(video.keywords)


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
        metadata = get_metadata(url_or_urlid)
        DbTools.insert( url_or_urlid,\
                        get_raw_subtitles( get_yt_sub_url( url_or_urlid ) ),\
                        get_title( metadata ),\
                        get_author( metadata ),\
                        get_length( metadata ),\
                        get_date( metadata ),\
                        get_category( metadata ),\
                        get_tags( metadata ),\
                        '0'\
                        )
    else:
        raise ValueError( "Failed to store '" + url_or_urlid + "': did not validate" )
