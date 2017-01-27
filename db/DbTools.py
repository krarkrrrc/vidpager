import CONST
import ScanTools #for search_all
from sqlalchemy import create_engine #motor
from sqlalchemy import MetaData #easy work with "structures"
from sqlalchemy import Table, Column #structure
from sqlalchemy import Integer, String, DateTime, Boolean #datatypes
from sqlalchemy import select #for reading

#metadata is collection of tables and can be traversed like XML DOM
metadata = MetaData()
#needed for all the defs to reference engine
engine = create_engine("sqlite:///" + CONST.db_name)

#schema, use foreignkeys, if we need to make relationship between tables
subtitles_table = Table("subtitles", metadata,
    Column("rowid", Integer, primary_key=True),
    Column("urlid", String),
    Column("captions", String),
    Column("timestamps", String),
    Column("title", String),
    Column("author", String),
    Column("length", Integer),
    Column("date", DateTime), #Was Integer
    Column("category", String),
    Column("tags", String),
    Column("asr", Boolean) #Was Integer
)


def init():
    #metadata.create_all(engine) creates everything where metadata is
    subtitles_table.create(engine) #creates just subtitles_table


def insert(table=None, *args, **kwargs):
    #TODO is this the right way?
    if table == 'subtitles':
        insert_to_subtitles( **kwargs )
    else:
        raise NotImplementedError( "table '" + table + "' not implemented" )

#insert function made this redundant
def insert_to_subtitles( **kwargs ) :
    """
    Inserts a complete row into a table
    video_data must be exact dict returned by bot
    """
    #TODO DON'T save same urlid twice, partially solved in try block in vidpager.py
    #print( kwargs['urlid'], kwargs['author'], kwargs['title'] )
    table_insert = Table.insert( subtitles_table ).values( **kwargs )
    engine.execute(table_insert)


def get_data(urlid, *keys):
    """
    Returns data from urlid
    """
    #TODO return more data at once, calling this often is probably expensive op
    select_by_urlid = select([subtitles_table]).\
    where(subtitles_table.c.urlid == urlid)
    result_row = engine.execute(select_by_urlid).fetchone()
    result = []
    for key in keys:
        result.append(result_row[key])
    return result


def search_all(target):
    urlids_with_subtitles = select([
    subtitles_table.c.urlid,
    subtitles_table.c.title,
    subtitles_table.c.author,
    subtitles_table.c.category]).\
    where(subtitles_table.c.asr == 0)
    raw_all = engine.execute(urlids_with_subtitles).fetchall()
    print('Searching in',len(raw_all),'entries')
    for row in raw_all:
        #rawall is a list with sqlalchemy.engine.result.RowProxy
        urlid = row.values()[0] #urlid is first in urlids_with_subtitles
        #row is rest of the select which the function can print
        ScanTools.search_text_and_print_metadata(urlid, target, row)
