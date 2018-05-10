from peewee import *
from goose import Goose
from datetime import datetime
from Incidents import *
import csv
import time

def mapToIncident(row):
	if not (row[9].isdigit()):
		row[9] = None
	if not (row[12].isdigit()):
		row[12] = None
	incident = Incident(City=row[3], State=row[4], Zip=row[5], Coordinates=row[6],
						VictimName=row[7], VictimGender=row[8], VictimAge=row[9],
						MotoristName=row[10], MotoristGender=row[11], MotoristAge=row[12],
						HitAndRun=row[13], ImpairedDriving=row[14], IncidentType=row[15],
						VehicleType=row[16], VehicleMake=row[17], VehicleModel=row[18])
	row[2] = row[2].strip()
	dateTimeStr = row[1] + ' ' + row[2]
	dateTimeStr = dateTimeStr.strip()

	if (row[2] != ''):
		dateTimeObj = datetime.datetime.strptime(dateTimeStr, '%m/%d/%Y %I:%M %p')
	else:
		dateTimeObj = datetime.datetime.strptime(dateTimeStr, '%m/%d/%Y')

	incident.IncidentDateTime = dateTimeObj
	return incident

def getSources(row):
	urlSources = row[19]
	return [x.strip() for x in urlSources.split(';') if x != '']	

def mapToIncidentSource(url, incident, count_obj):
	g = Goose()
	article = g.extract(url=url)

	try:
		incidentSource = IncidentSource(Incident=incident, URL=url, Domain=article.domain, ArticleText=article.cleaned_text.decode('utf8'), ArticleTitle=article.title.decode('utf8'))
		if (article.opengraph is not None) and ('site_name' in article.opengraph):
			incidentSource.Name = article.opengraph['site_name']

		incidentSource.save()	
		count_obj['incidentSourceCount'] += 1
	except Exception as e: 
		print e
		count_obj['errorCount'] += 1



with open('2017_data.tsv', 'rb') as csvfile:
	start_time = time.time()
	count_obj = {}
	count_obj['errorCount'] = 0
	count_obj['incidentCount'] = 0
	count_obj['incidentSourceCount'] = 0
	
	datafile = csv.reader(csvfile, delimiter='	')

	for row in datafile:
		print row
		count_obj['incidentCount'] += 1
		incident = mapToIncident(row)
		incident.save()
		sources = getSources(row)
		for url in sources:
			mapToIncidentSource(url, incident, count_obj)
	end_time = time.time()

	print '\n Job finished. Number of Incidents: ', count_obj['incidentCount'], 
	' Number of IncidentSources: ', count_obj['incidentSourceCount'] , 
	' Number of errors: ', count_obj['errorCount']
	print("Execution time was %g seconds" % (end_time - start_time))


