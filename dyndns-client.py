import argparse
from TinhatDyndns import client
from TinhatDyndns.client import IPDetector
from sys import platform

__author__ = 'christoph'

if platform == "linux" or platform == "linux2":
    gpg_binary_path = '/usr/bin/gpg'
elif platform == "darwin":
    gpg_binary_path = '/usr/bin/gpg'
elif platform == "win32":
    gpg_binary_path = '"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"'


parser = argparse.ArgumentParser(description='Manage hostnames of the tinhat dyndns server.')
parser.add_argument('--gpg-binary', nargs='?', help='the path to the gpg binary', default=gpg_binary_path)
parser.add_argument('--keys-directory', nargs='?', help='the directory which contains the keyring', required=True)
parser.add_argument('--service-host', nargs='?', help='the hostname of the dyndns service', default='dyndns.tinhat.de')
parser.add_argument('--service-port', nargs='?', help='the port of the dyndns service', default='80')
parser.add_argument('--ipv4-host', nargs='?', help='the hostname of the ipv4 service', default='lookup-ipv4.tinhat.de')
parser.add_argument('--ipv4-port', nargs='?', help='the port of the ipv4 service', default='80')
parser.add_argument('--ipv6-host', nargs='?', help='the hostname of the ipv6 service', default='lookup-ipv6.tinhat.de')
parser.add_argument('--ipv6-port', nargs='?', help='the port of the ipv6 service', default='80')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

parser_create = subparsers.add_parser('register', help='register a new hostname')
parser_create.add_argument('--hostname', help='the hostname to register', required=True)

parser_update = subparsers.add_parser('update', help='updates the ip addresses of a hostname')
parser_update.add_argument('--hostname', help='the hostname to update', required=True)
parser_update.add_argument('--ipv4', help='the ipv4 address or auto for automatic detection', default='auto')
parser_update.add_argument('--ipv6', help='the ipv6 address or auto to automatic detection', default='auto')

parser_query = subparsers.add_parser('query', help='queries a hostname')
parser_query.add_argument('--hostname', help='the hostname to query', required=True)

parser_delete = subparsers.add_parser('delete', help='deletes a hostname')
parser_delete.add_argument('--hostname', help='the hostname to query', required=True)

args = parser.parse_args()

service_client = client.Client(args.gpg_binary, args.keys_directory,args.service_host,args.service_port)

if args.command == 'register':
    service_client.create(args.hostname)
elif args.command == 'update':
    detector = IPDetector(args.ipv4_host, args.ipv4_port, args.ipv6_host, args.ipv6_port)
    if args.ipv4 == 'auto':
        ipv4 = detector.detect_ipv4_address()
    else:
        ipv4 = args.ipv4
    if args.ipv6 == 'auto':
        ipv6 = detector.detect_ipv6_address()
    else:
        ipv6 = args.ipv6
    service_client.update(args.hostname, ipv4, ipv6)
elif args.command == 'query':
    service_client.query(args.hostname)
elif args.command == 'delete':
    service_client.delete(args.hostname)

