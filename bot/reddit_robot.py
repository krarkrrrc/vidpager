#!/usr/bin/env python
import praw # to get links
import time # for wait loop
import operator #for sorting
from prawcore.exceptions import RequestException #to handle exceptions

"""search in any domain and any combinations of subreddits and return rdict
use praw.ini in the same root folder to configure your bot
see https://praw.readthedocs.io/en/latest/getting_started/authentication.html"""

#TODO
#return clean links
#pass category correctly
#since save_links overwrites the file, print some kind of diff
#links such as these bellow have to be resolved, they don't have yt_id
#    https://gaming.youtube.com/attribution_link?a=RLshOXtkiZI&u=%2Fuser%2FMadZombiie%2Flive

reddit = praw.Reddit('vidpager_reader')
reddit.read_only = True

max_limit = 300
#max_limit = 981 #it won't get higher, prints by 100 anyway
#with new, 5 is very high score
score_limit = 1
yt_domain1 = 'youtube.com'
yt_domain2 = 'youtu.be'
target_file = 'links'
verbose = True
wait_time = 300


def return_rdict(submission):
        return({
            'gold' : submission.gilded,
            'nsfw' : submission.over_18,
            'rlink' : submission.permalink,
            'rcomments_count' : submission.num_comments,
            'rid' : submission.id,
            'rsub' : submission.subreddit,
            'rtitle' : submission.title,
            'rscore' : submission.score,
            'rshortlink' : submission.shortlink,
            'url' : submission.url
            })

"""
reddit.domain categories:
    controversial
    hot
    new - full of all kinds of bull****
    rising - didn't work
    random_rising
    top
"""


def get_domain(domain, fk = 0, filter_by_score=False, category = 'hot'):
    result = {}
    for s in reddit.domain(domain).new(limit=max_limit):
        if filter_by_score:
            if s.score >= score_limit:
                result[fk] = return_rdict(s)
        else:
            result[fk] = return_rdict(s)
        fk += 1
    return result


def get_subreddit(subreddits, fk = 0, filter_by_score=False, category = 'hot'):
    result = {}
    target_subreddit = ''
    for sub in subreddits.split(','):
        target_subreddit += '+' + sub
    target_subreddit[1:]
    for s in reddit.subreddit(target_subreddit[1:]).new(limit=max_limit):
        if filter_by_score:
            if s.score >= score_limit:
                result[fk] = return_rdict(s)
        else:
            result[fk] = return_rdict(s)
        fk += 1
    return result


def compare_dicts(d1,d2):
    #TODO do it better!
    #pick larger dict, to avoid KeyError
    longest_d = max(len(d1),len(d2))
    if longest_d == len(d1):
        ld = d1
        sd = d2
    elif longest_d == len(d2):
        ld = d2
        sd = d1
    print('Diff is',len(ld) - len(sd))
    #collect list of same ids
    #TODO do one line fors here
    ld_rids = []
    for key in ld:
        ld_rids.append(ld[key]['rid'])
    sd_rids = []
    for key in sd:
        sd_rids.append(sd[key]['rid'])
    shared = set(ld_rids) & set(sd_rids)
    result = {}
    result_index = 0
    for key in ld:
        #TODO write comments what this does, i still don't know
        #sd is not called at all, wtf
       if not any(same_id in ld[key]['rid'] for same_id in shared):
           result[result_index] = ld[key]
           result_index += 1
    return result



def save_links(dict, verbose=True):
    stuff = {}
    for i in dict:
         stuff[i] = bunch[i]['rscore']
    sorted_by_lowest_score = sorted(stuff.items(), key=operator.itemgetter(1))
    if verbose:
        for index in sorted_by_lowest_score:
            #index is tupe with key and rscore
            #getting UnicodeError on Raspberry
            print("{0}|{1}|<{2}>"
            .format(index[1], dict[index[0]]['rtitle'],dict[index[0]]['url']))
    with open(target_file,'w') as f:
        for key, value in dict.items():
            f.write(dict[key]['url']+'\n')
    print('Saved {0} links'.format(len(dict)))

if __name__ == '__main__':
    def end_loop():
        global run
        print("This is run #{0} @{1}"
                .format(run,time.strftime("%H:%M:%S",time.localtime())))
        run += 1
    run = 0
    while True:
        print('Collecting new bunch')
        try:
            new_bunch = {}
            new_bunch_yt1 = get_domain(yt_domain1, fk = 0, filter_by_score=True)
            print('Got {0} items from {1}'.format(len(new_bunch_yt1), yt_domain1))
            new_bunch.update(new_bunch_yt1)
            new_bunch_yt2 = get_domain(yt_domain2, fk = len(new_bunch_yt1), filter_by_score=True)
            print('Got {0} items from {1}'.format(len(new_bunch_yt2), yt_domain2))
            new_bunch.update(new_bunch_yt2)
            new_bunch_subs = get_subreddit('videos,documentaries', fk = len(new_bunch), filter_by_score=True)
            print('Got {0} items from {1}'.format(len(new_bunch_subs), 'videos and documentaries'))
            new_bunch.update(new_bunch_subs)
        except RequestException as e:
            print('\n\nCAUGHT THE ERROR', e, '\n\n')
            continue
        if run == 0:
            #first run
            bunch = new_bunch
        else:
            #compare
            print('Comparing')
            if bunch == new_bunch: #simplest compare
                print('Run',run,'skipped, same dicts')
                end_loop()
                continue
            else:
                print('new dict differs, compare pls?')
                #proper compare
                #filter out same rids (reddit id)
                #TODO this results mess for now
                #bunch = compare_dicts(bunch,new_bunch)
                pass
        save_links(bunch,verbose=verbose)
        print("Sleeping for {0}m".format(round(wait_time/60)))
        end_loop()
        time.sleep(wait_time)