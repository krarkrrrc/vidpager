#!/usr/bin/env python
#for loading modules in folders
import sys
sys.path = ['.', '..'] + sys.path
import CONST
from bot import GetSubtitles #for getting yt data
from db import DbTools #for Db stuff
import ScanTools #for searching
import os.path #for checking if db exist
import re #for validate_yt_url

"""
Main entry point for program
"""
#TODO validate sys.argv[1], only string and spaces should be allowed
#TODO logging (only for storing cases, no need for search_all runs)


def search_one(input_url, target):
    # search vid for keyword provided from cmd line
    # TODO replace with ui print
    for match in ScanTools.text_search( input_url, target ):
        print("{0} - \"{1}\"\n"
        "{2}\n".format(match['timestamp'], match['caption'], match['url']))


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
        #check if input was whole url, get only last 11 characters
        input_url = parse_yt_url(input_url)
        if input_url is False:
            raise ValueError
        if DbTools.get_data(input_url, 'urlid') == input_url:
            print(input_url, 'is already stored.\n')
        else:
            subtitles_table_insert_data = GetSubtitles.store(input_url)
            if subtitles_table_insert_data:
                print('Saving subtitles data for video',input_url)
                DbTools.insert('subtitles_table',
                **subtitles_table_insert_data)
                #TODO skip searching if you just wan't to save
                #search_one(input, sys.argv[1])
            else:
                print('Failed to get data for insert')
    except IndexError:
        DbTools.search_all(sys.argv[1])
    except ValueError:
        #url not validated
        sys.exit(1)
