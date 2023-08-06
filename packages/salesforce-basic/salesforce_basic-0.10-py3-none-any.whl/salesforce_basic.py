from urllib.request import Request, urlopen
import logging
from urllib.parse import quote
from urllib.error import HTTPError
import os
from time import sleep
import json
import boto3
import pdb



logger = logging.getLogger(__name__)

class SFError(Exception):
    def __init__(self, text):
        self.text = text
        


class SalesforceBasicConnector:
    def __init__(self, sandbox = False, **kwargs):
        if 'client_id' not in kwargs:
            # this means that we get them from the aws parameter store
            aws_client = boto3.client('ssm', region_name = kwargs['region_name'])
            logging.info('getting client info from aws')
            kwargs = json.loads(aws_client.get_parameter(Name=kwargs['name'])['Parameter']['Value'])
        if sandbox:
            self.refresh_host = 'test.salesforce.com'
        else:
            self.refresh_host = 'login.salesforce.com'
        self.client_id = kwargs['client_id']
        self.client_secret = kwargs['client_secret']
        self.access_token = kwargs['access_token']
        self.refresh_token = kwargs['refresh_token']
        self.request_url = kwargs['instance_url']
        self.request_prefix = self.request_url + '/services/data/v44.0/'
        return

    def do_request(self, locator, refresh = False, data=None, method = 'POST', return_as_json = True, delete = False):
        if '/' == locator[0]:
            locator = locator[1:]
        if refresh:
            refresh_path = "https://%s/services/oauth2/token?grant_type=refresh_token&client_id=%s&client_secret=%s&refresh_token=%s" % (self.refresh_host, self.client_id, self.client_secret, self.refresh_token)
            response = urlopen(refresh_path)
            self.access_token = json.loads(response.read())['access_token']
            logger.info('did a refresh, got a new access token')
        request_string = self.request_prefix + locator
        logger.info('at=%s' % self.access_token)
        request = Request(request_string, headers = {'Authorization' : 'Bearer ' + self.access_token, 'content-type': 'application/json'})
        if 'POST' != method:
            request.get_method = lambda: method
        display_data = data
        if display_data and (200 < len(display_data)):
            display_data = display_data[:200] + b"..."
        logger.info('making request to %s with data %s' % (request_string, display_data))
        try:
            response = urlopen(request, data= data)
            code = response.getcode()
            data = response.read()
            if (200 <= code) and (299 >= code):
                if return_as_json:
                    data = json.loads(data)
                return data
            else:
                raise Exception("Expecting OK status, got %d (error: %s) from requesting: '%s'" % (code, data, request_string))
        except HTTPError as err:
            text = err.read()
            # raise if not 401 or 401 and refresh
            if refresh or (401 != err.code):
                logger.warning('got http err, code is: %d, reason: %s' % (err.code, text))
                logger.warning('raising error')
                raise SFError(text)
            else:
                logger.info('bad authorization, redoing request with refresh')
                return self.do_request(locator, refresh = True, data = data, return_as_json = return_as_json, method = method)
        return 
    
    def get_all_objects_of_type(self, fields, object_type):
        logger.info('querying fields %s of %s' % (fields, object_type))
        query_results = self.do_request("query/?q=%s" % quote("select %s From %s" % (','.join(fields), object_type)))
        while True:
            logger.info('Total %d, count %d objects, done:%s' % (query_results['totalSize'], len(query_results['records']), query_results['done']))
            for record in query_results['records']:
                yield record
            next_record_url = query_results.get('nextRecordsUrl', None)
            if next_record_url:
                next_record_url = next_record_url[next_record_url.index('query'):]
                query_results = self.do_request(next_record_url)
            else:
                break
        logger.info('finished finding objects')
        return




            
