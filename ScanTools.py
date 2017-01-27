from db import DbTools
import re
import CONST

"""
Contains tools to page/scan through a video in the db
TODO - candidate algorithm to search text w/o a vid id
"""

def text_search( urlid, text ):
    """
    returns a list of objects containing the matching caption and a timestamped url of the matching caption in the vid
    """
    #TODO allow to search full words only
    captions, timestamps = DbTools.get_data( urlid, 'captions','timestamps')
    query_patt = '(' + CONST.synctag_patt + ')(' + CONST.caption_patt + text + CONST.caption_patt + ')'
    caption_matches = re.findall( query_patt, captions )
    yt_path = 'http://www.youtube.com/watch?v=' + urlid + '&t='
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
    return re.sub( r'\\xe2\\x80\\x99', "'", re.sub( r'\\n', ' ', caption ) )

def search_text_and_print_metadata(urlid, target, metadata):
    """
    move this to ui
    urlid, target is for text_search
    metadata is list of metadata from select query
    """
    for index, match in enumerate(text_search(urlid, target)):
        #print header
        if index == 0:
            #metadata are based on DbTools.search_all
            #index1 = title, rest is self explanatory
            print("\n----- {0} -----".format(metadata[1]))
            #skip first two indexes
            for item in metadata[2:]:
                print("Author:", metadata[2])
                print("Category:", metadata[3])
                print("-----{0}-------\n".format(len(metadata[1]) * '-'))
                break
        #print titles
        print("{0} - \"{1}\"\n"
        "{2}\n".format(match['timestamp'], match['caption'], match['url']))
