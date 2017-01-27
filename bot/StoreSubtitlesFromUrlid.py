#!/usr/bin/env python
import sys
sys.path = ['.', '..'] + sys.path
import CONST
import re #for def store()
import datetime # for datetime
from db import DbTools #for def store()
from urllib.request import urlopen #to get subtitles
import pafy #for getting metadata


"""
V0.1 GET yt subtitles
V0.2 GET video metadata using pafy
V0.3 added parse{date,subtitles} from DBTools, store returns json
     if get_raw_subtitles returns false, report and set asr to True
example API url to get subtitles
https://www.youtube.com/api/timedtext?lang=en&v=3NxKH1MK4z8&fmt=vtt&name=
"""


def get_raw_subtitles(video_id):
    """
    return data from input_video url
    TODO better error handling
    """
    #yt API url to download subtitles in vtt format
    url = 'https://www.youtube.com/api/timedtext?lang=en&v='\
    + video_id + '&fmt=vtt&name='
    try:
        get = urlopen(url)
        data = get.read()
        if len(data) > 0:
            return data
        else:
            return False # no subtitles
    except ValueError:
        print('Unkown url',url)
        # TODO return error


def get_metadata(video_id):
    pafy.set_api_key(CONST.youtube_data_api_key)
    try:
        url = 'https://www.youtube.com/watch?v=' + video_id
        return pafy.new(url)
    except ValueError:
        print('Unkown url',url)
        # TODO return error

#not used
#TODO I am lame at raising errors, but KISS?
def get_date(video):
    date_str = video.published
    # verify date is valid
    try:
        datetime = parse_date( date_str )
    except TypeError as e:
        print( CONST.vp_error + 'invalid date found for title: ' + video.title )
    return datetime

def store(urlid):
    """
    store a videos subtitles by either a urlid or url (not yet implement)
    TODO write url_validate code
    """
    url_validate_test = False
    urlid_validate_test = re.search( '[\d\w]{11}', urlid )
    if ( url_validate_test ):
        pass
    elif ( urlid_validate_test ):
        metadata = get_metadata(urlid)
        raw_subs = get_raw_subtitles(urlid)
        if not raw_subs:
            print('Video {0} does not have any subtitles. Storing only metadata'
            .format(urlid))
            asr = True
        else:
            asr = False
        parsed_subs = parse_subtitles(raw_subs)
        return {
         'video_id' : urlid,
         'captions' : parsed_subs['captions'],
         'timestamps' : parsed_subs['timestamps'],
         'title' : metadata.title,
         'author' : metadata.author,
         'length' : metadata.length,
         'date' : parse_date(metadata.published),
         'category' : metadata.category,
         'tags' : ','.join(metadata.keywords),
         'asr' : asr
          }
    else:
        raise ValueError( "Failed to store '" + urlid + "': did not validate" )


def parse_subtitles( subtitles ):
    """
    returns dict of captions and timestamps from raw subtitles in vtt from youtube
    """
    # match[0] is timestamp, [1] is caption
    matches = re.findall( r'(\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d)\\n([\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+)\\n\\n', str(subtitles)[2:-1] )
    captions = ""
    timestamps = ""
    count = 0
    for match in matches:
        captions += '<' + str( count ) + '>' + match[1]
        timestamps += '<' + str( count ) + '>' + match[0]
        count += 1

    return { 'captions' : captions, 'timestamps' : timestamps }


def parse_date( date_str ):
    match = re.search( r'(\d{4})-(\d\d)-(\d\d)\s(\d\d):(\d\d):(\d\d)', date_str ).groups()
    print( 'match length is *****: ', len( match ) )
    try:
        date = datetime.datetime( int( match[0] ), int( match[1] ), int( match[2] ), int( match[3] ), int( match[4] ), int( match[5] ), tzinfo=datetime.timezone.utc )
    except TypeError as e:
        print( CONST.vp_error + 'valid date string not found in DbTools.parse_date()', e )
        raise e
    return date
