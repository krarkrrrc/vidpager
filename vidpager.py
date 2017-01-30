#!/usr/bin/env python
#for loading modules in folders
import sys
sys.path = ['.', '..'] + sys.path
import CONST
from bot import GetSubtitles #for getting yt data
from db import DbTools #for Db stuff
import ScanTools #for searching
import ui #for printing
import os.path #for checking if db exist
import re #for validate_yt_url

"""
Main entry point for program
"""
#TODO validate sys.argv[1], only string and spaces should be allowed
#TODO logging (only for storing cases, no need for search_all runs)


def parse_yt_url(url):
    if re.match('[\w\d\-]{11}', url):
        #input is yt_id
        return url
    #match only youtu.be/ID not:
    #https://m.youtube.com/watch?feature=youtu.be&v=yYAw79386WI
    elif 'youtu.be' in url and not 'feature=youtu.be' in url:
        match = re.search('\/([\w\d\-]{11})', url)
        if match != None:
            return match.group(1)
    elif 'youtube.com' in url:
        #TODO reddit_robot.py shouldn't give those
        if 'youtube.com/embed/' in url:
            match = re.search('\/([\w\d\-]{11})', url)
            if match != None:
                return match.group(1)
        if 'youtube.com/shared' in url:
            #match = re.search('ci\=([\w\d\-]{11})', url)
            match = re.search('shared\?ci\=([\w\d\-]{11})', url)
            if match != None:
                return match.group(1)
        if 'attribution_link' in url:
            #these vidoes can't be resolved
            print('SKIP:Attribution_link have to be resolved, meh this.')
            return False
        if 'youtube.com/playlist?list' in url:
            print("SKIP:Can't handle playlist links, yet.")
            #TODO ask youtube_robot to get all links
            return False
        if 'channel' in url:
            print("SKIP:Won't handle channel links.")
            return False
        if 'youtube.com/user' in url:
            print("SKIP:Won't handle user links")
        match = re.search('v\=([\w\d\-]{11})', url)
        if match != None:
            return match.group(1)
    else:
        print(url, 'is not YT, won\'t do those!')
        sys.exit(2)

if __name__ == '__main__':
    # make sure db exists, create one if not
    if not ( os.path.isfile( './' + CONST.db_name ) ):
        DbTools.init()

    #check if url(sys.argv[2]) is passed
    #TODO do args stuff properly
    try:
        input_url = sys.argv[2]
        #validate
        input_url = parse_yt_url(input_url)
        if input_url is False:
            raise ValueError #exit 1
        #check db for the id
        saved_urlid = DbTools.get_data(input_url, 'urlid')
        if saved_urlid is not False and saved_urlid[0] == input_url:
            #video saved, do search in it
            if sys.argv[1] != '^SAVE_ONLY^':
                ui.search_text_in_subtitles(input_url, sys.argv[1])
            else:
                #TODO is this bad? that this gets printed only with ^SAVE_ONLY^?
                print(input_url, 'is already stored.\n')
        else:
            #not saved, try to save
            print('Trying to save subtitle data for video',input_url)
            subtitles_table_insert_data = GetSubtitles.get_yt_dict(input_url, get_asr_subitles=True)
            if subtitles_table_insert_data:
                DbTools.insert('subtitles_table',
                **subtitles_table_insert_data)
            else:
                print('Failed to get data for insert')
    except IndexError:
        #only first arg passed
        DbTools.search_all(sys.argv[1])
    except ValueError:
        #url not validated
        sys.exit(1)
