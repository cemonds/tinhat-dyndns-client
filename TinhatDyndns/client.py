import gnupg
import httplib
import json
import os

__author__ = 'christoph'


class Client():
    def __init__(self, keys_directory, service_host, service_port):

        self.gpg = gnupg.GPG(gpgbinary='"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"',  gnupghome=keys_directory)
        self.gpg.encoding = 'utf-8'
        self.service_host = service_host
        self.service_port = service_port

    def create(self, hostname):
        input_data = self.gpg.gen_key_input(key_type="RSA", key_length=2048, name_real='dyndns key for hostname '+hostname)
        key = self.gpg.gen_key(input_data)
        ascii_armored_public_key = self.gpg.export_keys(key)
        message = {'publicKey': ascii_armored_public_key}
        json_message = json.dumps(message,separators=(',',':'))

        signature = self.gpg.sign(json_message, keyid=key, detach=True)
        conn = httplib.HTTPConnection(self.service_host, self.service_port)
        body = {'message':message, 'signature':signature.data}
        body_string = json.dumps(body,separators=(',',':'))

        conn.request("POST", "/hosts/"+hostname, body_string)
        response = conn.getresponse()
        if response.status == 201:
            print "hostname "+hostname+" successfully registered\n"
        else:
            print "ERROR: hostname "+hostname+" could not be registered, status "+str(response.status)+"\n"
    def query(self, hostname):
        print "query"
    def update(self, hostname, ipv4, ipv6):
        print "update"
    def delete(self, hostname):
        print "delete"



