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
    except sqlite3.OperationalError as e:
        print( '****', e, '\nCreating schemaversion table' )
        con.execute( '''CREATE TABLE IF NOT EXISTS schemaversion
                        ( rowid INTEGER PRIMARY KEY, version text)''' )
        version = "0.0"
        insert_args( version, table='schemaversion' )
        con.execute( '''CREATE TABLE IF NOT EXISTS subtitles
                        ( rowid INTEGER PRIMARY KEY, urlid text, captions text, timestamps text, title text, author text, length integer, date integer, category text, tags text, asr integer )''' )
        cursor = con.execute( "SELECT version FROM schemaversion WHERE rowid = 1" )
    version = cursor.fetchone()[0]
    print( 'initial database version = ', version )
    if version == "0.0":
        pass

def get_con():
    return sqlite3.connect( CONST.db_name )

def insert_args( *args,  table='subtitles', **kwargs ):
    """
    Inserts a complete row into a table, the rowid is automatically appended as NULL to the end
    """

    if table == 'subtitles':
        subs = str( args[1] )[2:-1]
        parsed_subs = parse_subtitles( subs ) 
        args = [ args[0], parsed_subs['captions'], parsed_subs['timestamps'], args[2], args[3], args[4], args[5], args[6], args[7], args[8] ]
    
    con = get_con()
    args_str = "','".join( args )

    try:
        with con:
            con.execute( "INSERT INTO " + table + " VALUES ( NULL, '" + args_str + "')" )
    except sqlite3.IntegrityError:
        print( "Error inserting into db" )


def get_rowid_from_urlid( urlid ):
    """
    Returns a row id to select columns from
    """
    con = get_con()

    try:
        with con:
            rowid = str( con.execute( "SELECT rowid FROM subtitles WHERE urlid =:urlid", {"urlid": urlid} ).fetchone()[0] )
    except sqlite3.IntegrityError:
        print( "Error in get_rowid_from_urlid" )
    #print( "rowid = " + str( rowid ) )
    return rowid

def get_column_from_rowid( rowid, column ):
    con = get_con()
    
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

def insert( *args, **kwargs ):
    if len( args ) == 9:
        insert_args( *args )
    elif len( kwargs ) == 9:
        urlid = kwargs['url_or_urlid'] 
        raw_subs = kwargs['raw_subs']
        title = kwargs['title']
        author = kwargs['author']
        length = kwargs['length']
        date = kwargs['date']
        category = kwargs['category']
        tags = kwargs['tags']
        asr = kwargs['asr']
        insert_args( urlid, raw_subs, title, author, length, date, category, tags, asr )
    else:
        raise ValueError( "Not enough arguments provided to DbTools.insert()" )
    return


