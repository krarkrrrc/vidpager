#!/usr/bin/env python
import CONST
from urllib.request import urlopen #to get subtitles
import pafy #for getting metadata
import re #for def store()
import datetime # for datetime

"""
V0.1 GET yt subtitles
V0.2 GET video metadata using pafy
V0.3 added parse{date,subtitles} from DBTools, store returns json
     if get_raw_subtitles returns false, report and set asr to True
V.04 set youtube_data_api_key at start and not in each get_metadata call
     parse_date works fine, no need to print the match length
     urlid_validate_test replaced by vidpager.parse_yt_url, gets verified before
example API url to get subtitles
https://www.youtube.com/api/timedtext?lang=en&v=3NxKH1MK4z8&fmt=vtt&name=
"""

pafy.set_api_key(CONST.youtube_data_api_key)


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
        return False


def store(urlid, get_asr_subtitles=False):
    """store a videos subtitles by urlid"""
    metadata = get_metadata(urlid)
    if not metadata:
        print('Youtube not avaliable or BIG FAIL, HANDLE IT!!!!!')
        return False
    result = {
    'author' : metadata.author,
    'category' : metadata.category,
    'date' : get_date(metadata),
    'length' : metadata.length,
    'tags' : ','.join(metadata.keywords),
    'title' : metadata.title,
    'urlid' : urlid
     }
    raw_subs = get_raw_subtitles(urlid)
    if not raw_subs:
        print('No subtitles avaliable, storing only metadata')
        asr = True
        if get_asr_subtitles:
            #TODO
            pass
        else:
            result['captions'] = ''
            result['timestamps'] = ''
    else:
        print('\nSubtitles avaliable!!!\n')
        asr = False
        parsed_subs = parse_subtitles(raw_subs)
        result['captions'] = parsed_subs['captions']
        result['timestamps'] = parsed_subs['timestamps']
    result['asr'] : asr
    return result


def get_date(video):
    """
    returns datetime.datetime object from pafy.new('videoid').published
    prints for which video (pafy.new object) the date is invalid
    """
    date_str = video.published
    # verify date is valid
    try:
        datetime = parse_date( date_str )
    except TypeError as e:
        print( CONST.vp_error + 'invalid date found for title: ' + video.title )
    return datetime


def get_metadata(video_id):
    try:
        url = 'https://www.youtube.com/watch?v=' + video_id
        return pafy.new(url)
    except ValueError:
        print('Unkown url', url)
        return False
    except OSError: #pafy error
        return False



def parse_date( date_str ):
    """
    Converts datetime string returned from pafy.new('videoid').published
    """
    match = re.search( r'(\d{4})-(\d\d)-(\d\d)\s(\d\d):(\d\d):(\d\d)', date_str ).groups()
    try:
        date = datetime.datetime(
        int( match[0] ), int( match[1] ), int( match[2] ), int( match[3] ),
        int( match[4] ), int( match[5] ), tzinfo=datetime.timezone.utc )
    except TypeError as e:
        print('{0} valid date string not found in '
              'StoreSubtitlesFromUrlid.parse_date() {1}'
              .format(CONST.vp_error, e))
        raise e
    return date


def parse_subtitles( subtitles ):
    """
    returns dict of captions and timestamps from subtitles in vtt from youtube
    """
    # match[0] is timestamp, [1] is caption
    matches = re.findall( CONST.raw_subs_patt, str(subtitles)[2:-1] )
    captions = ""
    timestamps = ""
    count = 0
    for match in matches:
        captions += '<' + str( count ) + '>' + match[1]
        timestamps += '<' + str( count ) + '>' + match[0]
        count += 1

    return { 'captions' : captions, 'timestamps' : timestamps }
