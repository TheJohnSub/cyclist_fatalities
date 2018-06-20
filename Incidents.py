import peewee 
import ConfigParser
from peewee import *
import datetime

config_parse = ConfigParser.ConfigParser()
config_parse.read('config.ini')

database = MySQLDatabase(config_parse.get('keys', 'database_name'), user=config_parse.get('keys', 'database_user'), passwd=config_parse.get('keys', 'database_passwd'))
database.connect()

class BaseModel(Model):
		class Meta:
			database = database

class BaseSource(BaseModel):
    URL = CharField(null = True)
    Name = CharField(null = True)
    Domain = CharField(null = True)
    ArticleTitle = TextField(null = True)
    ArticleText = TextField(null = True)

class Incident(BaseModel):
	IncidentDateTime = 	DateTimeField(null = True)
	City = CharField(null = True)
	State = CharField(null = True)
	Zip = CharField(null = True)
	Coordinates = CharField(null = True)
	VictimName = CharField(null = True)
	VictimGender = CharField(null = True)
	VictimAge = IntegerField(null = True)
	MotoristName = CharField(null = True)
	MotoristGender = CharField(null = True)
	MotoristAge = IntegerField(null = True)	
	HitAndRun = BooleanField(null = True)
	ImpairedDriving = BooleanField(null = True)
	IncidentType = CharField(null = True)
	VehicleType = CharField(null = True)
	VehicleMake = CharField(null = True)
	VehicleModel = CharField(null = True)

class IncidentSource(BaseSource):
    Incident = ForeignKeyField(Incident, related_name='Sources')

class UnrelatedSource(BaseSource):
	pass

class Scrub(BaseModel):
	RunDateTime = DateTimeField(null = True)
	NumCandidates = IntegerField(null = True)
	NumRelatedCandidates = IntegerField(null = True)
	ScrubType = CharField(null = True)
	ScrubTypeId = IntegerField(null = True)
	SearchKeywords = CharField(null = True)

class IncidentSourceCandidate(BaseSource):
	Scrub = ForeignKeyField(Scrub, related_name='Candidates')
	SearchFeedId = CharField(null = True)
	SearchFeedURL = TextField(null = True)
	SearchFeedText = TextField(null = True)
	SearchFeedJSON = TextField(null = True)
	IsRelated = BooleanField(null = True, default = False)

if not (Incident.table_exists() and IncidentSource.table_exists()):
	database.create_tables([Incident, IncidentSource])

if not (UnrelatedSource.table_exists()):
	database.create_table(UnrelatedSource)

if not (Scrub.table_exists()):
	database.create_table(Scrub)

if not (IncidentSourceCandidate.table_exists()):
	database.create_table(IncidentSourceCandidate)
