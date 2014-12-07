"""
Usage:
    NetGeo analyze [options] INPUT_FILE
    NetGeo translate [options] INPUT_FILE OUTPUT_FILE

Options:
    -o --output OUTPUT      output file [default: result.csv]
    --pingTime PING_TIME    number of used PING packets to estimate mean RTT [default: 4]
    -v --verbose            Print progress
    -h --help               shows this message and exit
    --version               shows program version
"""

from __future__ import print_function
from subprocess import Popen, PIPE
import csv
import json
import math
import re
import sys
import platform
import timeit
import urllib2
import socket

from docopt import docopt


EARTH_RADIUS = 6371.009
MAX_IP_LIST_SIZE = 1000
VERSION = '1.0.2'


def get_ip_address(url):
    result = None
    try:
        result = socket.gethostbyname(url)
    except socket.gaierror:
        pass
    return result


def translate_urls_to_ip(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            ip_address = get_ip_address(line.rstrip())
            if ip_address is not None:
                output_file.write('{}\n'.format(ip_address))


def get_host_location(ip_address=''):
    location = None
    try:
        resp = urllib2.urlopen('http://ipinfo.io{}/json'.format('' if ip_address == '' else '/{}'.format(ip_address)))
        if resp.getcode() == 200:
            json_result = json.loads(resp.read())
            if 'loc' in json_result and json_result['loc'] != '':
                location = tuple([math.radians(float(x)) for x in json_result['loc'].split(',')])
            else:
                print('Result does not contains localization info for ip address "{}"!'.format(ip_address), file=sys.stderr)
        else:
            print('WRN: Cannot estimate {0} location!'.format(ip_address), file=sys.stderr)
    except urllib2.HTTPError:
        pass
    return location


def get_distance(start, end):
    distance = None
    if start is not None and end is not None:
        delta_latitude = start[0] - end[0]
        mean_latitude = (start[0] + end[0]) / 2
        delta_longitude = start[1] - end[1]
        distance = EARTH_RADIUS * math.sqrt(delta_latitude ** 2 + (math.cos(mean_latitude) * delta_longitude) ** 2)
    else:
        print("WRN: Either home host or target host localization are not known! Cannot calculate distance!", file=sys.stderr)
    return distance


def get_mean_rtt(ip_address, deadline=5):
    mean_rtt = None
    system_type = platform.system()
    ping_command = None
    if system_type == 'Linux':
        ping_command = 'ping -qw {1} {0}'.format(ip_address, deadline)
    if ping_command is not None:
        ping_result = Popen(ping_command, shell=True, stdout=PIPE).stdout.read().splitlines()
        for line in ping_result:
            match = re.match('rtt min/avg/max/mdev = (?P<rttMin>.*)/(?P<rttAvg>.*)/(?P<rttMax>.*)/(?P<rttMdev>.*) ms', line)
            if match is not None:
                mean_rtt = match.group('rttAvg')
        if mean_rtt is None:
            print('WRN: Host {0} does not answer for PING!'.format(ip_address), file=sys.stderr)
    return mean_rtt


def get_hops_count(ip_address):
    result = None
    traceroute_command = None
    system_type = platform.system()
    if system_type == 'Linux':
        traceroute_command = 'traceroute {0}'.format(ip_address)
    if traceroute_command is not None:
        traceroute_result = Popen(traceroute_command, shell=True, stdout=PIPE).stdout.read().splitlines()
        result = len(traceroute_result[2:])
    return result


def get_download_time(ip_address):
    result = None
    try:
        start_time = timeit.default_timer()
        resp = urllib2.urlopen('http://{}'.format(ip_address))
        end_time = timeit.default_timer()
        if resp.getcode() == 200:
            result = (end_time - start_time) / len(resp.read())
        else:
            print('WRN: Cannot download default page from {0}'.format(ip_address), file=sys.stderr)
    except (urllib2.HTTPError, urllib2.URLError):
        print('WRN: Error while downloading default page from {0}'.format(ip_address), file=sys.stderr)
    return result


def main():
    args = docopt(__doc__, version=VERSION)
    verbose = args['--verbose']

    if args['analyze']:
        input_file_path = args['INPUT_FILE']
        output_file_path = args['--output']
        ping_time = args['--pingTime']

        if verbose:
            print('Getting home host localization')
        my_localization = get_host_location()
        if my_localization is not None:
            try:
                with open(output_file_path, 'w') as outputFile:
                    csv_writer = csv.writer(outputFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(('IP address', 'localization', 'distance', 'RTT time', 'hops count', 'downloading time'))
                    with open(input_file_path, 'r') as inputFile:
                        used_ip_addresses = []
                        for ip_address in [x.strip() for x in inputFile]:
                            if len(used_ip_addresses) < MAX_IP_LIST_SIZE:
                                if ip_address not in used_ip_addresses:
                                    used_ip_addresses.append(ip_address)
                                    if verbose:
                                        print('Processing {0}'.format(ip_address))
                                    target_localization = get_host_location(ip_address)
                                    distance = get_distance(my_localization, target_localization)
                                    mean_rtt = get_mean_rtt(ip_address, ping_time)
                                    hops_count = get_hops_count(ip_address)
                                    download_time = get_download_time(ip_address)
                                    csv_writer.writerow((ip_address, target_localization, distance, mean_rtt, hops_count, download_time))
                                else:
                                    print('WRN: IP address {0} has been checked before! Skipping'.format(ip_address), file=sys.stderr)
                            else:
                                print('WRN: Maximum number of tested IP addresses ({0}) was reached! Breaking'.format(MAX_IP_LIST_SIZE))
                                break
            except IOError:
                print('ERR: Input/output error!')
        else:
            print('ERR: Cannot estimate home host localization! Exiting', file=sys.stderr)

    elif args['translate']:
        input_file_path = args['INPUT_FILE']
        output_file_path = args['OUTPUT_FILE']
        translate_urls_to_ip(input_file_path, output_file_path)

if __name__ == '__main__':
    main()