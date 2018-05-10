from peewee import *
from goose import Goose
from datetime import datetime
from Incidents import *

text_file = open("unrelated_source_list.txt", "r")
url_list = text_file.readlines()

for url in url_list:
	g = Goose()
	article = g.extract(url=url)
	try:
		source = UnrelatedSource(URL=url, Domain=article.domain, ArticleText=article.cleaned_text, ArticleTitle=article.title)
		if (article.opengraph is not None) and ('site_name' in article.opengraph):
			source.Name = article.opengraph['site_name']

		source.save()	
		print source.ArticleTitle
	except Exception as e: 
		print e
