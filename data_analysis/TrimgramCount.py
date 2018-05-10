from peewee import *
import nltk
from nltk.collocations import *
from collections import Counter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Incidents import *

textBlock = ""
for source in IncidentSource.select():
	textBlock += source.ArticleText + '\n'

textBlock = textBlock.lower()

trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(textBlock.split())
finder.apply_freq_filter(10) 

ngrams = finder.nbest(trigram_measures.pmi, 100)  
for one, two, three in ngrams:
	print one, two, three

