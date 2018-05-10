from TwitterSearch import *

def contains_nonTwitter_domain(urls):
	success = False
	for url in urls:
		domainName = url['expanded_url']
		if (domainName.find('twitter.com') == -1):
			success = True
	return success

try:
    tso = TwitterSearchOrder() 
    tso.set_keywords(['cyclist', 'killed']) 
    tso.set_language('en') 
    tso.set_include_entities(True) 

    ts = TwitterSearch(
        consumer_key = 'FSRqsdZnVc0vQaosOjNE7Gb4z',
        consumer_secret = '8Vu8HqCXnVSuLvOZt3RJmlK8HVP9z5zsh7Qk9k4PcZjeNsAHnA',
        access_token = '1018148114-G4apdnYp0htOcwYb2CBhnZkI8d619T40g8jUNEM',
        access_token_secret = 'ZVwZGXmox8mxWYpQrC6A8BhfiFIbT7Q3jlLiXwUE1v1q4'
     )

    mysearchResp = ts.search_tweets(tso)
    contentOnly = mysearchResp['content']['statuses']
    filterResp = [x for x in contentOnly if len(x['entities']['urls']) > 0 and contains_nonTwitter_domain(x['entities']['urls'])]

    f = open('output.txt', 'w', encoding='utf8')
    f.write(str(filterResp))
    f.close()


except TwitterSearchException as e:
    print(e)


