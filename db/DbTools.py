import sys
import sqlite3
import CONST 
import re

"""
Provides the low-level functions to insert, query and update the db
"""

def init():
    con = sqlite3.connect( CONST.db_name )
    # asr value is auto-speech-recognition rendered captions, either 0 (false) or 1 (true)
    con.execute( '''CREATE TABLE IF NOT EXISTS subtitles
                    ( urlid text, title text, captions text, timestamps text, asr integer, ROWID INTEGER PRIMARY KEY )''' )
    return con

def insert( *args,  table='subtitles', **kwargs ):
    """
    Takes 3 arguments in the following order: String video_title, String url_id, String subtitles
    """
    con = init()

    try:
        with con:
            con.execute( "INSERT INTO " + table + " VALUES ( '" + args[0] + "', '" + args[1] + "', '" + args[2] + "', '" + args[3] + "', '" + args[4] + "', NULL )" )
    except sqlite3.IntegrityError:
        print( "Error inserting into db" )


def get_rowid_from_urlid( urlid ):
    """
    Returns a row id to select columns from
    """
    con = init()

    try:
        with con:
            rowid = str( con.execute( "SELECT rowid FROM subtitles WHERE urlid =:urlid", {"urlid": urlid} ).fetchone()[0] )
    except sqlite3.IntegrityError:
        print( "Error in get_rowid_from_urlid" )
    #print( "rowid = " + str( rowid ) )
    return rowid

def get_column_from_rowid( rowid, column ):
    con = init()    
    
    try:
        with con:
            column_data = str( con.execute( "SELECT " + column + " FROM subtitles WHERE rowid = " + rowid + ";" ).fetchone()[0] )
    except sqlite3.IntegrityError:
        print( "Error in get_column_from_rowid" )
    return column_data

def get_column_from_urlid( urlid, column ):
    return get_column_from_rowid( get_rowid_from_urlid( urlid ), column )

def parse_subtitles( subtitles ):
    # match[0] is timestamp, [1] is caption
    matches = re.findall( r'(\d\d:\d\d:\d\d\.\d\d\d\s-->\s\d\d:\d\d:\d\d\.\d\d\d)\\n([\w\s\d\\\,\.\;\:\$\!\%\)\(\?\/\'\"\-]+)\\n\\n', subtitles ) 
    captions = ""
    timestamps = ""
    count = 0
    for match in matches:
        captions += '<' + str( count ) + '>' + match[1]
        timestamps += '<' + str( count ) + '>' + match[0]
        count += 1

    return { 'captions' : captions, 'timestamps' : timestamps }

def insert_raw_subtitles( urlid, raw_subs, title ):
    subs = str( raw_subs )[2:-1]
    parsed_subs = parse_subtitles( subs ) 
    insert( urlid, title, parsed_subs['captions'], parsed_subs['timestamps'], '0') 

