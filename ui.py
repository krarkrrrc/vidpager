import ScanTools
from db import DbTools #how to import only something if DbTools is in db folder?


def search_all_and_print(target):
    """searches subs in all entries"""
    urlids_with_metadata = DbTools.select([
    DbTools.subtitles_table.c.urlid, #row[0]
    DbTools.subtitles_table.c.title, #row[1]
    DbTools.subtitles_table.c.author, #row[2]
    DbTools.subtitles_table.c.category]) #row[3]
    raw_all = DbTools.engine.execute(urlids_with_metadata).fetchall()
    print('Searching in',len(raw_all),'entries')
    mentions = 0
    for row in raw_all:
        #TODO what is the difference between row[0] and row.values()[0]?
        #rawall is a list with sqlalchemy.engine.result.RowProxy
        search = ScanTools.text_search(row[0], target)
        if search:
            mentions += len(search) #TODO is it ok to count mentions like that?
            for index, match in enumerate(search):
                #print header
                if index == 0:
                    print("\n----- {0} -----".format(row[1])) #title
                    for item in row[2:]: #skip first two indexes
                        print("Author:", row[2])
                        print("Category:", row[3])
                        print("-----{0}-------\n".format(len(row[1]) * '-'))
                        break
                print_subtitles(match)
    print("There are {0} mentions of {1} in DB.".format(mentions, target))


def search_text_in_subtitles(input_url, search_string):
    """search vid for keyword provided from cmd line and urlid"""
    search = ScanTools.text_search(input_url, search_string )
    if search:
        for match in search:
            print_subtitles(match)
    else:
        #in case of single search it makes sense to print nothing found
        print('No mention of "{0}" mentioned in YT video {1}'
        .format(search_string, input_url))


def print_subtitles(match):
    print("{0} - \"{1}\"\n"
    "{2}\n".format(match['timestamp'], match['caption'], match['url']))
