from subprocess import Popen, PIPE
import csv, json, math
import os, platform
import re
import timeit
import urllib2

EARTH_RADIUS = 6371.009
OUTPUT_FILE_NAME = 'result.csv'

def getHostLocation(ipAddr = ''):
	location = None
	try:
		resp = urllib2.urlopen('http://ipinfo.io{}/json'.format('' if ipAddr == '' else '/{}'.format(ipAddr)))
		if resp.getcode() == 200:
			jsonResult = json.loads(resp.read())
			if 'loc' in jsonResult and jsonResult['loc'] != '':
				location = tuple([math.radians(float(x)) for x in jsonResult['loc'].split(',')])
			else:
				print 'Result does not contains localization info for ip address "{}"!'.format(ipAddr)
		else:
			print 'Cannot fetch host location!'
	except urllib2.HTTPError:
		pass
	return location

def getDistance(start, end):
	deltaLatitude = start[0] - end[0]
	meanLatitude = (start[0] + end[0]) / 2
	deltaLongitude = start[1] - end[1]
	distance = EARTH_RADIUS * math.sqrt(deltaLatitude**2 + (math.cos(meanLatitude) * deltaLongitude)**2)
	return distance

def getMeanRTT(ipAddress, count=4):
	meanRTT = None
	systemType= platform.system()
	pingCommand = None
	if systemType == 'Linux':
		pingCommand = 'ping -q -c {1} {0}'.format(ipAddress, count)
	if pingCommand != None:
		pingResult = Popen(pingCommand, shell=True, stdout=PIPE).stdout.read().splitlines()
		for line in pingResult:
			match = re.match('rtt min/avg/max/mdev = (?P<rttMin>.*)/(?P<rttAvg>.*)/(?P<rttMax>.*)/(?P<rttMdev>.*) ms', line)
			if match != None:
				meanRTT = match.group('rttAvg')
	return meanRTT

def getDownloadTime(ipAddr):
	result = None
	try:
		startTime = timeit.default_timer()
		resp = urllib2.urlopen('http://{}'.format(ipAddr))
		endTime = timeit.default_timer()
		if resp.getcode() == 200:
			result = (endTime - startTime) / float(resp.headers['content-length'])
	except urllib2.HTTPError:
		pass
	return result

def main(ipAddressesList=['212.77.100.101']):
	myLocalization = getHostLocation()
	outputFilePath = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
	with open(outputFilePath, 'w') as outputFile:
		csvWriter = csv.writer(outputFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvWriter.writerow(('IP address', 'localization', 'distance', 'RTT time', 'downolading time'))
		for ipAddress in ipAddressesList:
			targetLocalization = getHostLocation(ipAddress)
			distance = getDistance(myLocalization, targetLocalization)
			meanRTT = getMeanRTT(ipAddress)
			downloadTime = getDownloadTime(ipAddress)
			csvWriter.writerow((ipAddress, targetLocalization, distance, meanRTT, downloadTime))

if __name__ == '__main__':
	main()