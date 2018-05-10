import sys
import ConfigParser
from TwitterSearch import *
from peewee import *
from goose import Goose
from datetime import datetime
from Incidents import *
sys.path.insert(0, 'source_recognition') 
from source_recognition import *

def contains_nonTwitter_domain(urls):
    success = False
    url = get_expanded_url(urls)
    if (url.find('twitter.com') == -1):
        success = True
        return success

def get_expanded_url(urls):
    for url in urls:
        expanded_url = url['expanded_url']
        return expanded_url

def get_tweet_url(json_node):
    tweet_id = json_node['id_str']
    user_handle = json_node['user']['id_str']
    return 'https://www.twitter.com/' + user_handle + '/status/' + tweet_id

def run_tweet_scrub(keywords):
    print 'Running scrub for keywords: ' + str(keywords)
    try:
        tso = TwitterSearchOrder() 
        tso.set_keywords(keywords) 
        tso.set_language('en') 
        tso.set_include_entities(True) 

        config_parse = ConfigParser.ConfigParser()
        config_parse.read('config.ini')

        ts = TwitterSearch(
            consumer_key = config_parse.get('keys', 'consumer_key'),
            consumer_secret = config_parse.get('keys', 'consumer_secret'),
            access_token = config_parse.get('keys', 'access_token'),
            access_token_secret = config_parse.get('keys', 'access_token_secret'),
         )

        scrub = Scrub(RunDateTime=datetime.datetime.now(), ScrubType='Twitter', ScrubTypeId=1, SearchKeywords=', '.join(keywords))
        scrub.save()

        mysearchResp = ts.search_tweets(tso)
        contentOnly = mysearchResp['content']['statuses']
        filter_resp = [x for x in contentOnly if len(x['entities']['urls']) > 0 and contains_nonTwitter_domain(x['entities']['urls'])]
        single_node = filter_resp[2]
        num_related = 0
        scrub.NumCandidates = len(filter_resp)

        for candidate in filter_resp:
            twit_url = get_expanded_url(candidate['entities']['urls'])
            if IncidentSourceCandidate.select().where(IncidentSourceCandidate.URL == twit_url).count() > 0:
                print('Continued on URL: ' + twit_url)
                continue

            g = Goose()
            article = g.extract(url=twit_url)
            try:
                twit_id = candidate['id']
                source_candidate = IncidentSourceCandidate(URL=twit_url, Domain=article.domain, ArticleText=article.cleaned_text.encode('utf8'), ArticleTitle=article.title.encode('utf8'), Scrub=scrub, SearchFeedId=twit_id, SearchFeedURL=get_tweet_url(candidate), SearchFeedText=candidate['text'].encode('utf8'))

                source_candidate.SearchFeedJSON = candidate
                if (article.opengraph is not None) and ('site_name' in article.opengraph):
                    source_candidate.Name = article.opengraph['site_name']
                if source_is_related(source_candidate):
                    source_candidate.IsRelated = True
                    num_related += 1
                source_candidate.save()
                print(source_candidate.SearchFeedText)
            except Exception as e:
                print(twit_url)
                print(type(article.cleaned_text))
                print(e)

        scrub.NumRelatedCandidates = num_related
        scrub.save()

    except TwitterSearchException as e:
        print(e)

    print '\n'
    print '--------------------------------------'

file_name = sys.argv[1]
text_file = open(file_name, "r")
text_list = text_file.readlines()
for line in text_list:
    keywords = line.split()
    run_tweet_scrub(keywords)