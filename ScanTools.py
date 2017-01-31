import CONST
from db import DbTools #for getting captions and timestamps
import re #for searching

"""
Contains tools to page/scan through a video in the db
TODO - candidate algorithm to search text w/o a vid id
"""


def text_search( urlid, text ):
    """
    returns a list of objects containing the matching caption and a timestamped url of the matching caption in the vid
    """
    #TODO allow to search full words only
    yt_path = 'http://www.youtube.com/watch?v=' + urlid + '&t='
    #get data, perhaps try?
    captions, timestamps = DbTools.get_data( urlid, 'captions','timestamps')
    query_patt = re.compile(
    '('+CONST.synctag_patt +')('+CONST.caption_patt+text+CONST.caption_patt+')',
    re.I)
    caption_matches = re.findall( query_patt, captions )
    if len(caption_matches) == 0:
        #nothing found
        return False
    urls = []
    tag = 0
    caption = 1
    for match in caption_matches:
        urls.append({
        'url': yt_path + get_time_parameter( match[tag], timestamps ),
        'caption': clean_caption( match[caption] ),
        'timestamp': get_raw_timestamp( match[tag], timestamps )
        })
    return urls

def get_raw_timestamp( tag, timestamps ):
    return re.search( '(' + tag + ')(' + CONST.timestamp_patt + ')', timestamps ).group(2)

def get_time_parameter( tag, timestamps ):
    time_segments = get_raw_timestamp( tag, timestamps )[:12].split( ':' )
    return time_segments[0] + 'h' + time_segments[1] + 'm' + str( round( float( time_segments[2] ) ) ) + 's'

def clean_caption( caption ):
    #TODO needs some optimization, but probably the subtitles are just bandly converted in bot/GetSubtitles.get_raw_subtitles?
    return re.sub( r'\\xe2\\x80\\x99', "'", re.sub( r'\\n', ' ', caption ) )
