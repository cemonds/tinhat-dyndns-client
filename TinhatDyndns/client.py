import gnupg
import httplib
import os

__author__ = 'christoph'


class Client():
    def create(self, hostname):
        print "create"
    def query(self, hostname):
        print "query"
    def update(self, hostname, ipv4, ipv6):
        print "update"
    def delete(self, hostname):
        print "delete"


PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
gpg = gnupg.GPG(gpgbinary='"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"',  gnupghome=os.path.join(PROJECT_PATH, 'keys'))
gpg.encoding = 'utf-8'



conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason


