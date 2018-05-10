from peewee import *
import nltk
from nltk.collocations import *
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Incidents import *

textBlock = ""
for source in IncidentSource.select():
	textBlock += source.ArticleText + '\n'
	#textBlock += source.ArticleTitle + '\n'

textBlock = textBlock.lower()
stemmer = PorterStemmer()


tokens = word_tokenize(textBlock.lower())
tokens_stemmed = []
for token in tokens:
	stemmed_token = stemmer.stem(token)
	tokens_stemmed.append(stemmed_token)


bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens_stemmed)
#trigram_measures = nltk.collocations.TrigramAssocMeasures()
#finder = TrigramCollocationFinder.from_words(tokens_stemmed)
finder.apply_freq_filter(5) 



ngrams = finder.nbest(bigram_measures.pmi, 100)  
for one, two in ngrams:
	print one, two

