import gnupg
import httplib
import os

__author__ = 'christoph'


class Client():
    def __init__(self, keys_directory):
        self.gpg = gnupg.GPG(gpgbinary='"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"',  gnupghome=keys_directory)
        self.gpg.encoding = 'utf-8'

    def create(self, hostname):
        print "create"
    def query(self, hostname):
        print "query"
    def update(self, hostname, ipv4, ipv6):
        print "update"
    def delete(self, hostname):
        print "delete"

conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason


