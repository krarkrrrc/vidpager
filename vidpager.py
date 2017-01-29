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
    elif 'youtube.com' in url:
        if 'attribution_link' in url:
            #these vidoes can't be resolved
            print('Attribution_link have to be resolved, meh this.')
            return False
            #TODO reddit_robot.py should skip those
        if 'playlist' in url:
            print("Can't handle playlist links, yet.")
            #TODO ask youtube_robot to get all links
            return False
        if 'channel' in url:
            print("Won't handle channel links.")
            return False
        youtube_r = 'v\=([\w\d\-]{11})'
        """works for:
        https://www.youtube.com/watch?v=m7B4JZAiG6c&index=17&list=PLRdw3IjKY2glNAk65mMuKe8Fy45-gFjxL
        https://www.youtube.com/watch?v=G9ebXtXO4lI&list=PLbVLa0kaymjgeExcgT-FGNRNvv_b-84lh&index=320
        https://www.youtube.com/watch?v=NTh6tlNkpwc&feature=share
        """
        match = re.search(youtube_r, url)
        if match != None:
            return match.group(1)
    #TODO elif youtu.be??
    else:
        print(url, 'is not handled TODO!')

if __name__ == '__main__':
    # make sure db exists, create one if not
    if not ( os.path.isfile( './' + CONST.db_name ) ):
        DbTools.init()

    #check if url(sys.argv[2]) is passed
    #TODO perhaps there is better way then with  tries?
    try:
        input_url = sys.argv[2]
        #validate
        input_url = parse_yt_url(input_url)
        if input_url is False:
            raise ValueError
        #check db for the id
        saved_urlid = DbTools.get_data(input_url, 'urlid')
        if saved_urlid is not False and saved_urlid[0] == input_url:
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
        DbTools.search_all(sys.argv[1])
    except ValueError:
        #url not validated
        sys.exit(1)
