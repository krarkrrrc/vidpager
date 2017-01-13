import sys
import sqlite3

conn = sqlite3.connect( "vidpager.db" )
c = conn.cursor()
#c.execute( "CREATE TABLE IF NOT EXISTS subtitles" )

c.execute( '''CREATE TABLE IF NOT EXISTS subtitles
             (title text, subtitles text, link text)''' )

c.execute( "INSERT INTO subtitles VALUES ( '" + sys.argv[1] + "', '" + sys.argv[2] + "', '" + sys.argv[3] + "' )" )

conn.commit()
conn.close()
