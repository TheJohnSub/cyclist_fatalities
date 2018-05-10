from peewee import *
from collections import Counter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Incidents import *

fullText = ""
for source in IncidentSource.select():
	fullText += source.ArticleText + '\n'

fullText = fullText.lower()
wordList = fullText.split()
wordCount = Counter(wordList)

for key, value in wordCount.most_common(200):
	print key, value