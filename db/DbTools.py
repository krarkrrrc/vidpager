import CONST
from sqlalchemy import create_engine #motor
from sqlalchemy import MetaData #easy work with "structures"
from sqlalchemy import Table, Column #structure
from sqlalchemy import Integer, String, DateTime, Boolean #datatypes
from sqlalchemy import select #for reading

#TODO DON'T save same urlid twice, partially solved in try block in vidpager.py
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


#TODO I am not sure about what **kwars would be for here
def insert(video_data,  table=subtitles_table, **kwargs):
    """
    Inserts a complete row into a table
    video_data must be exact dict returned by bot
    """
    subtitle_insert = Table.insert(table).values(
        urlid = video_data['video_id'],
    	captions = video_data['captions'],
    	timestamps = video_data['timestamps'],
    	title = video_data['title'],
    	author = video_data['author'],
    	length = video_data['length'],
    	date = video_data['date'],
    	category = video_data['category'],
    	tags = video_data['tags'],
    	asr = video_data['asr']
    )
    engine.execute(subtitle_insert)


def get_data(urlid, data):
    """
    Returns data from urlid
    """
    #TODO return more data at once, calling this often is probably expensive op
    select_by_urlid = select([subtitles_table]).\
    where(subtitles_table.c.urlid == urlid)
    result = engine.execute(select_by_urlid)
    return result.fetchone()[data]
