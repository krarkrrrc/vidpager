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
    #con.execute( "CREATE TABLE IF NOT EXISTS schemaversion
    #              ( version real )" )
    try:
        cursor = con.execute( "SELECT version FROM schemaversion WHERE rowid = 1" )
        version = cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        if ( e.args[0] == 'no such table: schemaversion' ):
            con.execute( '''CREATE TABLE IF NOT EXISTS schemaversion
                          ( rowid INTEGER PRIMARY KEY, version text)''' )
            version = "0.0"
            insert( version, table='schemaversion' )
    con.execute( '''CREATE TABLE IF NOT EXISTS subtitles
                    ( rowid INTEGER PRIMARY KEY, urlid text, title text, captions text, timestamps text, asr integer )''' )
    print( 'initial database version = ', version )
    if version == "0.0":
        con.execute( '''ALTER TABLE subtitles
                        ADD version TEXT;''' )
        con.execute( '''UPDATE schemaversion
                        SET version = '0.1';''' )
    return con

def insert( *args,  table='subtitles', **kwargs ):
    """
    Inserts a complete row into a table, the rowid is automatically appended as NULL to the end
    """
    con = init()
    args_str = ','.join( args )

    try:
        with con:
            con.execute( "INSERT INTO " + table + " VALUES ( 'NULL, " + args_str + "')" )
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
    """
    I don't think this belongs in DbTools
    """
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

