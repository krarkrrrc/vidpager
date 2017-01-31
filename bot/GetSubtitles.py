#!/usr/bin/env python
import CONST
from urllib.request import urlopen #to get subtitles
from urllib.error import HTTPError
import pafy #for getting metadata
import re #for parsing subtitles
import datetime #for datetime
import subprocess #for ask_youtube_dl_for_auto_subs_subtitles
from os import rename, remove, path #for ask_youtube_dl_for_auto_subs_subtitles

"""
V0.1 GET yt subtitles
V0.2 GET video metadata using pafy
V0.3 added parse{date,subtitles} from DBTools, store returns json
     if get_raw_subtitles returns false, report and set asr to True
V0.4 set youtube_data_api_key at start and not in each get_metadata call
     parse_date works fine, no need to print the match length
     urlid_validate_test replaced by vidpager.parse_yt_url, gets verified before
V0.5 ask_youtube_dl_for_auto_subs_subtitles
     differentiate between parse error and no auto subs subtitles avaliable
example API url to get subtitles
https://www.youtube.com/api/timedtext?lang=en&v=3NxKH1MK4z8&fmt=vtt&name=
"""

pafy.set_api_key(CONST.youtube_data_api_key)


def get_raw_subtitles(video_id):
    """return data from input_video url"""
    #yt API url to download subtitles in vtt format
    url = 'https://www.youtube.com/api/timedtext?lang=en&v='\
    + video_id + '&fmt=vtt&name='
    try:
        get = urlopen(url)
        data = get.read()
        if len(data) > 0:
            #TODO check if it gets converted properly
            #convert to string and normalize new lines
            return str(data).replace('\\n','\n')
        else:
            return False # no subtitles
    except HTTPError as he:
        print('url', url, 'returned' ,he)
        return False
    except ValueError:
        print('Unkown url',url)
        return False


def get_metadata(video_id):
    """run pafy.new.url(video_id)"""
    #this does not handle videos with shared, for some reason
    #https://www.youtube.com/shared?ci=MAgxWmjPDhQ Captain Picard's best inspirational speeches
    #which links to https://www.youtube.com/watch?v=Jph2qWXJ-Tk
    #TODO try to find by title same video
    try:
        url = 'https://www.youtube.com/watch?v=' + video_id
        return pafy.new(url)
    except ValueError:
        print('Unkown url', url)
        return False
    except OSError: #pafy error
        #TODO handle exact issue
        return False


def get_yt_dict(urlid, get_auto_subs=False):
    """store a videos subtitles by urlid
    if get_auto_subs is true:
        ytdl will be used to try to get
        automaticly recognized subtitles and if video does not have them
        only metadata are saved
    else:
        no metadata are saved"""


    def save_empty_subs():
        #otherwise these would be saved as NULL
        print('No subtitles avaliable, storing only metadata')
        result['captions'] = ''
        result['timestamps'] = ''


    metadata = get_metadata(urlid)
    if not metadata:
        #TODO save somewhere that this is has issue like this, so its skipped
        print('\nDEBUG: Youtube not avaliable or BIG FAIL, HANDLE IT!!!!!\n')
        return False
    #TODO handle errors for parse_date
    #parsed_date = parse_date(metadata.published), #return datetime.datetime in utc
    #if parsed_date is False:
        #parse_date = ''
    result = {
    'author' : metadata.author,
    'category' : metadata.category,
    'date' : parse_date(metadata.published), #return datetime.datetime in utc
    'length' : metadata.length,
    'tags' : ','.join(metadata.keywords), # convert the list to str
    'title' : metadata.title,
    'urlid' : urlid
     }
    raw_subs = get_raw_subtitles(urlid)
    if not raw_subs:
        auto_subs = True
        if get_auto_subs:
            try:
                parsed_auto_subs = ask_youtube_dl_for_auto_subs_subtitles(urlid)
            except ValueError: #returned if ytdl returns 0 but no file is loaded
                print('Video does not have auto subs.')
                #TODO download audio and make it yourself, NOPE!
                #this could be saved to yt videos with no subtitles (they could appear in future tho)
                save_empty_subs()
                result['asr'] = auto_subs
                return result
            if parsed_auto_subs:
                result['captions'] = parsed_auto_subs['captions']
                result['timestamps'] = parsed_auto_subs['timestamps']
            else:
                print('\nDEBUG: Fail to pass subtitles, FIX!!!\n')
                return False
        else:
            #not trying to save auto_subs subtitles
            save_empty_subs()
            result['asr'] = auto_subs
            return result
    else:
        print('\nSubtitles avaliable!!!\n')
        auto_subs = False
        parsed_subs = parse_subtitles(raw_subs)
        if parsed_subs:
           result['captions'] = parsed_subs['captions']
           result['timestamps'] = parsed_subs['timestamps']
        else:
            print("\n\nparsing of SAVED subs didn't work FIX!!!\n\n")
            return False
    result['asr'] = auto_subs
    return result


def ask_youtube_dl_for_auto_subs_subtitles(urlid):
    """call ytdl, download auto subs and clean them so they can be parsed"""

    def load_and_clean_subtitles_file(target_file):
        with open(target_file, 'r') as f:
            raw_subtitle_data = f.read()
        #probably static
        c1 = raw_subtitle_data.replace('<c>','').replace(' </c>','').replace('</c>','')
        c2 = c1.replace('<c.colorE5E5E5>','').replace('<c.colorCCCCCC>','')
        c3 = c2.replace(' align:start position:19%','') #have to do re
        c4 = c3.replace(' align:start position:0%','')
        c5 = c4.replace(' align:start position:0% line:0%','')
        c6 = c5.replace('&gt;&gt; ','')
        final = c6
        result = ''
        for line in final.split('\n'):
            if line.startswith('00"'): #replace with re somehow or set?
                result += line + '\n'
            else:
                filt = re.sub('\<\d\d:\d\d:\d\d\.\d\d\d\>', '', line)
                result += filt + '\n'
        return result


    #TODO pls do this pythonic way
    #maybe needed?
    # --sub-lang en (other languages are ugly translate)
    # --convert-subs vtt
    # with no -o passed, default format would be:
    # target_file = metadata['title'] + '-' + metadata['urlid'] + '.en.vtt'
    #TODO ffmpeg -i target_file output.srt, which does better cleaning
    #TODO don't save in dirs, that is just for debug, don't wanan bother with directories
    if urlid.startswith('-'):
        #see https://github.com/rg3/youtube-dl#how-do-i-download-a-video-starting-with-a--
        ytdl_asubs = ['youtube-dl', 'https://www.youtube.com/watch?v=' + urlid,'--write-auto-sub','--skip-download', '-otest_subs/'+urlid]
    else:
        ytdl_asubs = ['youtube-dl', urlid,'--write-auto-sub','--skip-download', '-otest_subs/'+urlid]
    ytdl_process = subprocess.run(ytdl_asubs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "[info] Writing video subtitles to" in str(ytdl_process.stdout):
        print('Subtitles downloaded')
    if "Couldn't find automatic captions" in str(ytdl_process.stderr):
        raise ValueError
    #if GOT b"WARNING: Couldn't find automatic captions for 4PyvR05vrC8\n"
    #then you are sure it can be flagged as that
    print('\n\nOUT',str(ytdl_process.stdout),'\n\n')
    print('\n\nERR',str(ytdl_process.stderr),'\n\n')
    if ytdl_process.returncode == 0:
        target_file = 'test_subs/' + urlid + '.en.vtt'
        if path.isfile(target_file):
            print('Subtitles are in',target_file,'Loading')
            subtitle_data = load_and_clean_subtitles_file(target_file)
            parsed_subs = parse_subtitles(subtitle_data)
            if parsed_subs:
                #success
                print("Auto subs extracted")
                #remove(target_file) #file processed, clean
                #for debug
                rename(target_file, 'done_subs/' + target_file.replace('test_subs/',''))
                return parsed_subs
            else:
                print("DEBUG: Auto subs extract fail.")
                return False
        else:
            print('Failed to find file',target_file)
        print('Downloaded but no file? Probably not available, OR HANDLE!!!')
        return False
    else:
        print("\nDEBUG: ytdl didn't return 0, what's wrong?\n")
        return False


def parse_subtitles( subtitles ):
    """
    returns dict of captions and timestamps from subtitles in vtt from youtube
    """
    # match[0] is timestamp, [1] is caption
    #matches = re.findall( CONST.raw_subs_patt, str(subtitles)[2:-1] )
    matches = re.findall(CONST.raw_subs_patt, subtitles)
    if len(matches) == 0:
        return False
    captions = ""
    timestamps = ""
    count = 0
    for match in matches:
        captions += '<' + str( count ) + '>' + match[1]
        timestamps += '<' + str( count ) + '>' + match[0]
        count += 1
    else:
        return { 'captions' : captions, 'timestamps' : timestamps }

def parse_date(date_str):
    """
    Converts string (e.g 2017-01-30 00:47:44) to datetime.datetime
    returned from pafy.new('videoid').published
    """
    pattern = pattern = '%Y-%m-%d %H:%M:%S'
    try:
        date = datetime.datetime.strptime(date_str, pattern)
        return date.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        print('pattern does not match')
        return False

def old_get_date(video):
    def old_parse_date( date_str ):
        """Converts datetime string (e.g 2017-01-30 00:47:44)
        returned from pafy.new('videoid').published"""
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
    """
    returns datetime.datetime object from pafy.new('videoid').published
    prints for which video (pafy.new object) the date is invalid
    """
    date_str = video.published
    # verify date is valid
    try:
        datetime = old_parse_date( date_str )
    except TypeError as e:
        print( CONST.vp_error + 'invalid date found for title: ' + video.title )
    return datetime
