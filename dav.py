from datetime import datetime
import caldav
import string
from caldav.elements import dav, cdav
from caldav.lib.namespace import ns
import itertools

# Caldav url
#url = "http://localhost:5232/user/"

now = datetime.now()
year = now.year
month = now.month
day = now.day

year2 = year + 100


def startcal(calendar_url, calendar_username, calendar_password, calendar_proxy):
	url = calendar_url
	proxy = calendar_proxy
	username = calendar_username
	password = calendar_password
	client = caldav.DAVClient(url, proxy, username, password)
	principal = client.principal()
	calendars = principal.calendars()
	return calendars

def printcal(calendars):
	eventinfoparsed = []
	ausgabe = ""
	if len(calendars) > 0:
		calendar = calendars[0]
		results = calendar.date_search(datetime(year, month, day), datetime(year2, month, day))
	#	print results
		for event in results:
			eventinfo = event.data.split("\n")
	#		print eventinfo
			z = 0
			for id, info in enumerate(eventinfo):
				if info == "END:VEVENT":
					break
				elif "BEGIN:VEVENT" in info:
					z = 1
				if z == 1:
					eventinfoparsed.append(info)
		eventinfoparsed2 = isplit(eventinfoparsed, "BEGIN:VEVENT")
	#	print eventinfoparsed2
		for lists in eventinfoparsed2:
			created = u""
                        uid = u""
                        start = u""
                        end = u""
                        summary = u""
                        location = u""
			for sublistvalue in lists:
				sublistvalue = unicode(sublistvalue)
				splitted = sublistvalue.split(":")
				if "CREATED" in splitted[0]:
					splitted.pop(0)
					created = " ".join(splitted)
					created = stripletters(created)
					created = maketimeviewable(created)
					created = " (Erstellt am " + created + ") " 
				if "UID" in splitted[0]:
                                        splitted.pop(0)
                                        uid = " ".join(splitted)
					uid = " (" + uid + ")"
				if "DTSTART" in splitted[0]:
                                        splitted.pop(0)
                                        start = " ".join(splitted)
                                        start = stripletters(start)
					start = maketimeviewable(start)
					start = "Beginn: " + start
				if "DTEND" in splitted[0]:
                                        splitted.pop(0)
                                        end = " ".join(splitted)
					end = stripletters(end)
					end = maketimeviewable(end)
					end = " Ende: " + end 
				if "SUMMARY" in splitted[0]:
                                        splitted.pop(0)
                                        summary = " ".join(splitted)
					summary = "<" + summary + "> "
				if "LOCATION" in splitted[0]:
                                        splitted.pop(0)
                                        location = " ".join(splitted)
					location = " Ort: " + location
			ausgabe =  summary + start + end + location  + created + "\n" + ausgabe # add uid if you need
	return ausgabe
			
def isplit(iterable,splitters):
	return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

def maketimeviewable(time):
	return time[:4] + "-" + time[4:6] + "-" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + ":" + time[12:14]

def stripletters(tostrip):
	all=string.maketrans('','')
        nodigs=all.translate(all, string.digits)
	nodigs = nodigs.decode('unicode-escape')
	to = u""
	translate_table = dict((ord(char), to) for char in nodigs)
	return tostrip.translate(translate_table)


#test = startcal(url, username, password, proxy)
#print printcal(test)

