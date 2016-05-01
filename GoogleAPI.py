#!/usr/bin/env python
from __future__ import print_function
import sys, httplib2, os, warnings
from pprint import pprint
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from ConfigParser import SafeConfigParser
try:
    import simplejson as json
except ImportError:
    import json

# until we get off 2.6 
warnings.filterwarnings("ignore", category=DeprecationWarning)

class GoogleAPI:
    def __init__(self, sub, conf='wmtconf/default.conf'):
        self._load_configs(conf)
        self._load_creds(sub)
        self._set_proxy()
        try:
            #build api service object
            self.service = build(self.conf["GoogleAPI"]["api"], self.conf["GoogleAPI"]["version"], http=self.http_auth)
        except Exception as e:
            print("Error obtaining credentials:\n({0}".format(repr(e)))

    def _load_configs(self, conf):
        c = SafeConfigParser()
        try:
            with open(conf) as fp:
                c.readfp(fp)
            self.conf = dict([(section, dict([(key, value) for key, value in c.items(section)])) for section in c.sections()])
        except Exception as e:
            print(e)

    def _load_creds(self, sub):
        #get keyfile to sign credentials with
        try:
            with open(self.conf["GoogleAPI"]["key_file"]) as f:
                self.conf["private_key"] = f.read()
            self.credentials = SignedJwtAssertionCredentials(
                self.conf["GoogleAPI"]["client_email"],
                self.conf["private_key"],
                [value for key, value in self.conf["scope"].items()],
                sub=sub)
        except Exception as e:
            print(e)
    
    def _set_proxy(self):
        try:
            os.environ["http_proxy"] = "http://{host}:{port}".format(**self.conf["proxy"])
            os.environ["https_proxy"] = "https://{host}:{port}".format(**self.conf["proxy"])
            self.http_auth = self.credentials.authorize(httplib2.Http(
                    timeout=5,
                    disable_ssl_certificate_validation=True))
        except KeyError as ke:
            self.http_auth = self.credentials.authorize(httplib2.Http())
        except Exception as e:
            print(e)
