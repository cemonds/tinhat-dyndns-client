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
        input_data = self.gpg.gen_key_input(key_type="RSA", key_length=2048, name_real=self.name_of_key(hostname), name_email='')
        key = self.gpg.gen_key(input_data)
        ascii_armored_public_key = self.gpg.export_keys(key)
        message = {'publicKey': ascii_armored_public_key}

        signed_message = self.sign_message(message, key)
        response = self.send_signed_message_via_method(signed_message, 'POST', hostname)

        if response.status == 201:
            print 'hostname {} successfully registered\n'.format(hostname)
        else:
            print 'ERROR: hostname {} could not be registered, status {}\n{}'.format(hostname, str(response.status), response.read())

    def query(self, hostname):
        print "query"

    def update(self, hostname, ipv4, ipv6):
        print "update"

    def delete(self, hostname):
        key_name = self.name_of_key(hostname)
        private_keys = self.gpg.list_keys(True)

        for key in private_keys:
            for uid in key['uids']:
                if key_name in uid:
                    message = {'confirm': 'delete'}

                    signed_message = self.sign_message(message, key['keyid'])
                    response = self.send_signed_message_via_method(signed_message, 'DELETE', hostname)
                    if response.status == 204:
                        self.gpg.delete_keys(key['fingerprint'], True)
                        print 'hostname {} successfully deleted\n'.format(hostname)

                    else:
                        print 'ERROR: hostname {} could not be deleted, status {}\n{}'.format(hostname, str(response.status), response.read())
                    return
        print 'ERROR: no key found for hostname {}'.format(hostname)

    def name_of_key(self, hostname):
        return 'dyndns key for hostname "{}"'.format(hostname)

    def sign_message(self, message, key):
        json_message = json.dumps(message,separators=(',',':'))
        signature = self.gpg.sign(json_message, keyid=key, detach=True)
        return {'message':message, 'signature':signature.data}

    def send_signed_message_via_method(self, message, method, hostname):
        path = '/hosts/{}'.format(hostname)
        body_string = json.dumps(message,separators=(',',':'))
        conn = httplib.HTTPConnection(self.service_host, self.service_port)
        conn.request(method, path, body_string)
        return conn.getresponse()

