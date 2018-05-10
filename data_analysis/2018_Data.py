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

def getRedditLink(link_Text, link_URL):
	linkStr = '[' + link_Text + ']'
	linkStr += '(' + link_URL + ')'
	return linkStr


with open('2018_January_Data.tsv', 'rb') as csvfile:
	start_time = time.time()
	count_obj = {}
	count_obj['errorCount'] = 0
	count_obj['incidentCount'] = 0
	count_obj['incidentSourceCount'] = 0
	
	datafile = csv.reader(csvfile, delimiter='	')
	print 'Location|Date|Cyclist Name|Sources'
	print ':-:|:-:|:-:|:-:'

	for row in datafile:
		count_obj['incidentCount'] += 1
		incident = mapToIncident(row)
		#incident.save()
		sources = getSources(row)
		
		incidentStr = '';
		loc_link = 'https://www.google.com/maps/place/' + incident.Coordinates.replace(" ", "")
		incidentStr = getRedditLink(incident.City + ', ' + incident.State + ' ' + incident.Zip, loc_link)
		incidentStr += '|' + incident.IncidentDateTime.strftime("%m/%d/%Y")
		if incident.VictimName.strip():
			incidentStr += '|' + incident.VictimName
		else:
			incidentStr += '|Unknown'
		if incident.VictimAge is not None:
			incidentStr += ' (' + str(incident.VictimAge) + ')'
		
		sourceStr = '|'
		source_count = 0
		for url in sources:
			source_count += 1
			sourceStr += ' ' + getRedditLink(str(source_count), url)
		
		print incidentStr + ' ' + sourceStr
	end_time = time.time()

	print '\n Job finished. Number of Incidents: ', count_obj['incidentCount'], 
	' Number of IncidentSources: ', count_obj['incidentSourceCount'] , 
	' Number of errors: ', count_obj['errorCount']
	print("Execution time was %g seconds" % (end_time - start_time))


