import CONST
import ui #for search_all
from sqlalchemy import create_engine #motor
from sqlalchemy import MetaData #easy work with "structures"
from sqlalchemy import Table, Column #structure
from sqlalchemy import Boolean, DateTime, Integer, String, Unicode #datatypes
from sqlalchemy import select #for reading
from sqlalchemy.exc import NoSuchColumnError #for bad call of get_data

#metadata is collection of tables and can be traversed like XML DOM
metadata = MetaData()
#TODO use conn and execute sql via connection and handle close when all is done
#TODO first vidpager.py must handle multiple queries
#needed for all the defs to reference engine
#TODO make get_data same way as insert
#TODO search_all with smart get_data call, see ui.search_text_in_subtitles
engine = create_engine("sqlite:///" + CONST.db_name)

#schema, use foreignkeys, if we need to make relationship between tables
subtitles_table = Table("subtitles", metadata,
    Column("rowid", Integer, primary_key=True),
    Column("urlid", String),
    Column("captions", Unicode),
    Column("timestamps", Unicode),
    Column("title", Unicode),
    Column("author", String),
    Column("length", Integer),
    Column("date", DateTime),
    Column("category", String),
    Column("tags", String),
    Column("asr", Boolean) #rename the value to auto_subs
)


def init():
    #metadata.create_all(engine) creates everything where metadata is
    subtitles_table.create(engine) #creates just subtitles_table


def insert(table=None, *args, **kwargs):
    if table == 'subtitles_table':
        #video_data must be exact dict returned by bot/GetSubtitles.get_yt_dict
        #print( kwargs['urlid'], kwargs['author'], kwargs['title'] )
        #TODO DON'T save same urlid twice, partially solved in try block in vidpager.py
        table_insert = Table.insert(subtitles_table).values( **kwargs)
    else:
        raise NotImplementedError( "table '" + table + "' not implemented" )
    #TODO try, results n stuff
    engine.execute(table_insert)


def get_data(urlid, *keys):
    """
    Returns data from urlid
    """
    #TODO return more data at once, calling this often is probably expensive op
    select_by_urlid = select([subtitles_table]).\
    where(subtitles_table.c.urlid == urlid)
    #TODO why fetchone?
    result_row = engine.execute(select_by_urlid).fetchone()
    if result_row:
        result = []
        for key in keys:
            try:
                result.append(result_row[key])
            except NoSuchColumnError as NSCE:
                print(NSCE)
                return False
        return result
    else:
        return False
