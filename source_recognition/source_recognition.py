import nltk
import string
import re
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.collocations import *
import os
import sys

def source_is_related(source):
	if (determine_source_related(source)):
		return True
	else:
		print source.ArticleTitle
		return False

def source_is_unrelated(source):
	if (determine_source_related(source)):
		print source.ArticleTitle
		return False
	else:
		return True

def determine_source_related(source):
	if (title_contains_related_phrase(source)):
		return True
	elif (article_contains_related_phrase(source)):
		return True
	else:
		return False

def is_phrase_in_text(file_name, source_text):
	stemmer = PorterStemmer()
	text_file = open(file_name, "r")
	text_list = text_file.readlines()
	phrase_list = []
	for phrase in text_list: #all phrases in list NEED to be lower case by default
		phrase = phrase.strip()
		phrase_list.append(phrase)
	source_tokens = word_tokenize(source_text.lower())
	source_tokens_stemmed = []
	for token in source_tokens:
		stemmed_token = stemmer.stem(token)
		source_tokens_stemmed.append(stemmed_token)

	full_source_stemmed = ' '.join(word for word in source_tokens_stemmed)
	for phrase in phrase_list:
		re_phrase = re.compile(phrase)
		if re_phrase.search(full_source_stemmed):
			return True
	return False	

def article_contains_related_phrase(source):
	source_text = source.ArticleText.lower()
	try:
		return is_phrase_in_text("source_recognition/text_phrases_cyclist.txt", source_text) and is_phrase_in_text("source_recognition/text_phrases_fatality.txt", source_text)
	except:
		print 'An Exception: ', source.ArticleTitle

	return False

def title_contains_related_phrase(source):
	source_text = source.ArticleTitle.replace("'", "").replace(",", "").lower()
	source_text = ''.join([i for i in source_text if not i.isdigit()])
	try:
		return is_phrase_in_text("source_recognition/title_phrases.txt", source_text)
	except:
		print 'An Exception: ', source.ArticleTitle
	return False