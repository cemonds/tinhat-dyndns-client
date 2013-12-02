import gnupg
import httplib
import json
import os

__author__ = 'christoph'

class IPDetector():
    def __init__(self,ipv4_service_host, ipv4_service_port, ipv6_service_host, ipv6_service_port):
        self.ipv4_service_host = ipv4_service_host
        self.ipv4_service_port = ipv4_service_port
        self.ipv6_service_host = ipv6_service_host
        self.ipv6_service_port = ipv6_service_port

    def detect_ipv4_address(self):
        connection = httplib.HTTPConnection(self.ipv4_service_host, self.ipv4_service_port)
        return self.check_response(connection)

    def detect_ipv6_address(self):
        connection = httplib.HTTPConnection(self.ipv6_service_host, self.ipv6_service_port)
        return self.check_response(connection)

    def check_response(self, connection):
        try:
            connection.request('GET', '/')
            response = connection.getresponse()
            if response.status != 200:
                return None
            else:
                return response.read().strip()
        except:
            return None


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
        response = self.send_signed_message_via_method('', 'GET', hostname)
        if response.status == 200:
            print 'hostname {} found\n{}'.format(hostname, response.read())
        elif response.status == 404:
            print 'hostname {} not found\n{}'.format(hostname, response.read())
        else:
            print 'ERROR: could not query hostname {}, status {}\n{}'.format(hostname, str(response.status), response.read())

    def update(self, hostname, ipv4, ipv6):
        key = self.find_key_for_hostname(hostname)
        if key:
            keyid = key['keyid']

            message = {'ipv4': ipv4,'ipv6':ipv6}

            signed_message = self.sign_message(message, keyid)
            response = self.send_signed_message_via_method(signed_message, 'PUT', hostname)
            if response.status == 204:
                print 'hostname {} successfully updated to {}(ipv4) and {}(ipv6)\n'.format(hostname,ipv4,ipv6)
            else:
                print 'ERROR: hostname {} could not be updated, status {}\n{}'.format(hostname, str(response.status), response.read())
        else:
            print 'ERROR: no key found for hostname {}'.format(hostname)

    def delete(self, hostname):
        key = self.find_key_for_hostname(hostname)
        if key:
            keyid = key['keyid']
            fingerprint = key['fingerprint']

            message = {'confirm': 'delete'}

            signed_message = self.sign_message(message, keyid)
            response = self.send_signed_message_via_method(signed_message, 'DELETE', hostname)
            if response.status == 204:
                self.gpg.delete_keys(fingerprint, True)
                print 'hostname {} successfully deleted\n'.format(hostname)

            else:
                print 'ERROR: hostname {} could not be deleted, status {}\n{}'.format(hostname, str(response.status), response.read())
        else:
            print 'ERROR: no key found for hostname {}'.format(hostname)

    def name_of_key(self, hostname):
        return 'dyndns key for hostname "{}"'.format(hostname)

    def find_key_for_hostname(self, hostname):
        key_name = self.name_of_key(hostname)
        private_keys = self.gpg.list_keys(True)
        for key in private_keys:
            for uid in key['uids']:
                if key_name in uid:
                    return key
        return None


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

