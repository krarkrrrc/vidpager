import sys
import sqlite3

def insert( *args,  table='subtitles', **kwargs ):
    """
    Takes 3 arguments in the following order: String video_title, String url_id, String subtitles
    """
    for val in args:
        print( val )
    con = sqlite3.connect( "vidpager.db" )
    con.execute( '''CREATE TABLE IF NOT EXISTS subtitles
                    (title text, url_id text, subtitles text)''' )
    #c = con.cursor()
    #c.execute( "CREATE TABLE IF NOT EXISTS subtitles" )
    try:
        with con:
            con.execute( "INSERT INTO " + table + " VALUES ( '" + args[0] + "', '" + args[1] + "', '" + args[2] + "' )" )
    except sqlite3.IntegrityError:
        print( "Error inserting into db" )
