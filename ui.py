import ScanTools


def print_subtitles(match):
    print("{0} - \"{1}\"\n"
    "{2}\n".format(match['timestamp'], match['caption'], match['url']))


def search_text_and_print_metadata(urlid, target, metadata):
    """
    urlid, target is for text_search
    metadata is list of metadata from select query
    """
    #TODO get metadata nicer, see DbTools.search_all
    for index, match in enumerate(ScanTools.text_search(urlid, target)):
        #print header
        if index == 0:
            #metadata are based on DbTools.search_all
            #index1 = title, rest is self explanatory
            print("\n----- {0} -----".format(metadata[1]))
            #skip first two indexes
            for item in metadata[2:]:
                print("Author:", metadata[2])
                print("Category:", metadata[3])
                print("-----{0}-------\n".format(len(metadata[1]) * '-'))
                break
        print_subtitles(match)


def search_text_in_subtitles(input_url, search_string):
    """search vid for keyword provided from cmd line"""
    search = ScanTools.text_search( input_url, search_string )
    if len(search) == 0:
        print('No results')
    else:
        for match in search:
            print_subtitles(match)
