import argparse
from TinhatDyndns import client

__author__ = 'christoph'

parser = argparse.ArgumentParser(description='Manage hostnames of the tinhat dyndns server.')
parser.add_argument('--keys-directory', nargs='?', help='the directory which contains the keyring', required=True)
parser.add_argument('--service-host', nargs='?', help='the hostname of the dyndns service', default='dyndns.tinhat.de')
parser.add_argument('--service-port', nargs='?', help='the port of the dyndns service', default='80')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

parser_create = subparsers.add_parser('register', help='register a new hostname')
parser_create.add_argument('--hostname', help='the hostname to register', required=True)

parser_update = subparsers.add_parser('update', help='updates the ip addresses of a hostname')
parser_update.add_argument('--hostname', help='the hostname to update', required=True)
parser_update.add_argument('--ipv4', help='the ipv4 address', required=True)
parser_update.add_argument('--ipv6', help='the ipv6 address')

parser_create = subparsers.add_parser('query', help='queries a hostname')
parser_create.add_argument('--hostname', help='the hostname to query', required=True)

parser_create = subparsers.add_parser('delete', help='deletes a hostname')
parser_create.add_argument('--hostname', help='the hostname to query', required=True)

args = parser.parse_args()

service_client = client.Client(args.keys_directory,args.service_host,args.service_port)

if args.command == 'register':
    print args.command
    service_client.create(args.hostname)
elif args.command == 'update':
    print args.command
elif args.command == 'query':
    print args.command
elif args.command == 'delete':
    print args.command

