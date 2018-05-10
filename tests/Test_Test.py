import sys
from Incidents import *
sys.path.insert(0, 'SourceRecognition') 
from source_recognition import *

def test_sources():
	failed_count = 0
	total_count = 0
	for source in IncidentSource.select().where(IncidentSource.ArticleTitle != "" and IncidentSource.ArticleText != ""):
		if source_is_related(source) == False:
			failed_count += 1
		total_count += 1
	print failed_count
	print total_count

	assert failed_count <= 0

def test_unrelated_sources():
	failed_count = 0
	for source in UnrelatedSource.select():
		if source_is_unrelated(source) == False:
			failed_count += 1
	print failed_count
	assert failed_count <= 0	
