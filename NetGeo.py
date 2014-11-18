"""
Usage: NetGeo.py [-hv -o OUTPUT -i INPUT --pingTime PING_COUNT] 

Options:
    -o --output OUTPUT      output file [default: result.csv]
    -i --input INPUT        input file [default: input.txt]
    -h --help               shows help and exit
    -v --verbose            Print progress
    --pingTime PING_TIME    number of used PING packets to estimate mean RTT [default: 4]
	
"""

from __future__ import print_function
from docopt import docopt
from subprocess import Popen, PIPE
import csv, json, math
import re
import sys, os, platform
import timeit
import urllib2

EARTH_RADIUS = 6371.009
MAX_IP_LIST_SIZE = 1000

def getHostLocation(ipAddr = ''):
	location = None
	try:
		resp = urllib2.urlopen('http://ipinfo.io{}/json'.format('' if ipAddr == '' else '/{}'.format(ipAddr)))
		if resp.getcode() == 200:
			jsonResult = json.loads(resp.read())
			if 'loc' in jsonResult and jsonResult['loc'] != '':
				location = tuple([math.radians(float(x)) for x in jsonResult['loc'].split(',')])
			else:
				print('Result does not contains localization info for ip address "{}"!'.format(ipAddr), file=sys.stderr)
		else:
			print('WRN: Cannot estimate {0} location!'.format(ipAddr), file=sys.stderr)
	except urllib2.HTTPError:
		pass
	return location

def getDistance(start, end):
	distance = None
	if start != None and end != None:
		deltaLatitude = start[0] - end[0]
		meanLatitude = (start[0] + end[0]) / 2
		deltaLongitude = start[1] - end[1]
		distance = EARTH_RADIUS * math.sqrt(deltaLatitude**2 + (math.cos(meanLatitude) * deltaLongitude)**2)
	else:
		print("WRN: Either home host or target host localization are not known! Cannot calculate distance!", file=sys.stderr)
	return distance

def getMeanRTT(ipAddr, deadline=5):
	meanRTT = None
	systemType= platform.system()
	pingCommand = None
	if systemType == 'Linux':
		pingCommand = 'ping -qw {1} {0}'.format(ipAddr, deadline)
	if pingCommand != None:
		pingResult = Popen(pingCommand, shell=True, stdout=PIPE).stdout.read().splitlines()
		for line in pingResult:
			match = re.match('rtt min/avg/max/mdev = (?P<rttMin>.*)/(?P<rttAvg>.*)/(?P<rttMax>.*)/(?P<rttMdev>.*) ms', line)
			if match != None:
				meanRTT = match.group('rttAvg')
		if meanRTT == None:
			print('WRN: Host {0} does not answer for PING!'.format(ipAddr), file=sys.stderr)
	return meanRTT

def getDownloadTime(ipAddr):
	result = None
	try:
		startTime = timeit.default_timer()
		resp = urllib2.urlopen('http://{}'.format(ipAddr))
		endTime = timeit.default_timer()
		if resp.getcode() == 200:
			result = (endTime - startTime) / len(resp.read())
		else:
			print('WRN: Cannot download default page from {0}'.format(ipAddr), file=std.stderr)
	except (urllib2.HTTPError, urllib2.URLError):
		print('WRN: Error while downloading default page from {0}'.format(ipAddr), file=sys.stderr)
	return result

def main(inputFilePath, outputFilePath, pingTime, verbose):
	if verbose:
		print('Geting home host localization')
	myLocalization = getHostLocation()
	if myLocalization != None:
		with open(outputFilePath, 'w') as outputFile:
			csvWriter = csv.writer(outputFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csvWriter.writerow(('IP address', 'localization', 'distance', 'RTT time', 'downlading time'))
			with open(inputFilePath, 'r') as inputFile:
				usedIpAddresses = []
				for ipAddress in [x.strip() for x in inputFile]:
					if len(usedIpAddresses) < MAX_IP_LIST_SIZE:
						if ipAddress not in usedIpAddresses:
							usedIpAddresses.append(ipAddress)
							if verbose:
								print('Processing {0}'.format(ipAddress))
							targetLocalization = getHostLocation(ipAddress)
							distance = getDistance(myLocalization, targetLocalization)
							meanRTT = getMeanRTT(ipAddress, pingTime)
							downloadTime = getDownloadTime(ipAddress)
							csvWriter.writerow((ipAddress, targetLocalization, distance, meanRTT, downloadTime))
						else:
							print('WRN: IP address {0} has been checked before! Skipping'.format(ipAddress), file=sys.stderr)
					else:
						print('WRN: Maximum number of tested IP addresses ({0}) was reached! Breaking'.format(MAX_IP_LIST_SIZE))
						break
	else:
		print('ERR: Cannot estimate home host localization! Exiting', file=sys.stderr)

if __name__ == '__main__':
	args = docopt(__doc__)
	main(args['--input'], args['--output'], args['--pingTime'], args['--verbose'])