from subprocess import Popen, PIPE
import csv
import json
import math
import os
import re
import timeit

EARTH_RADIUS = 6371.009
OUTPUT_FILE_NAME = 'result.csv'

def getHostLocation(ipAddr = ''):
	hostInfo = json.loads(Popen('curl -s ipinfo.io{}/json'.format('' if ipAddr=='' else '/{}'.format(ipAddr)), shell=True, stdout=PIPE).stdout.read())
	location = tuple([math.radians(float(x)) for x in hostInfo['loc'].split(',')])
	return location

def getDistance(start, end):
	deltaLatitude = start[0] - end[0]
	meanLatitude = (start[0] + end[0]) / 2
	deltaLongitude = start[1] - end[1]
	distance = EARTH_RADIUS * math.sqrt(deltaLatitude**2 + (math.cos(meanLatitude) * deltaLongitude)**2)
	return distance

def getMeanRTT(ipAddress, count=4):
	meanRTT = None
	pingResult = Popen('ping -q -c {} {}'.format(count, ipAddress), shell=True, stdout=PIPE).stdout.read().splitlines()
	for line in pingResult:
		match = re.match('rtt min/avg/max/mdev = (?P<rttMin>.*)/(?P<rttAvg>.*)/(?P<rttMax>.*)/(?P<rttMdev>.*) ms', line)
		if match != None:
			meanRTT = match.group('rttAvg')
	return meanRTT

def getDownloadTime(ipAddr):
	startTime = timeit.default_timer()
	Popen('wget {} -O /dev/null -q'.format(ipAddr), shell=True).wait()
	endTime = timeit.default_timer()
	return endTime - startTime

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