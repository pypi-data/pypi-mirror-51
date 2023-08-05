import hmac
import hashlib 
import binascii
import requests
import time
from platform import platform
from urllib.parse import urlencode

class WebCubers:
    module_name = 'WCPM'
    module_version = '1.8.1'
    module_http_header = {}
    base_url = 'https://portal.webcubers.com/api/v1/'

    def __init__(self, username, api_key):
        self.is_authenticated = False
        self.api_key = api_key
        self.api_username = username
        self.module_http_header['User-Agent'] = f'{WebCubers.module_name}/{WebCubers.module_version} ({platform()};)'
        
        check_login = self.__authenticate(username)
        if check_login['status']:
            self.is_authenticated = True
        else:
            self.error = {}
            self.error['message'] = check_login['message']
            self.error['code'] = check_login['code']

    def snippet(self, snippet_id):
        return self.__request('snippet', 'post', {'snippet_id' : snippet_id})
    
    def snippets(self):
        return self.__request('snippets')

    def repository(self, filename=None):
        return self.__request('repository')

    def repository_get(self, filename):
        return self.__request('repository/get', 'post', {'filename' : filename})

    def repository_post(self, filename, code, force=False):
        return self.__request('repository/post', 'post', {'filename' : filename, 'code': code, 'force': force})

    def profile(self):
        return self.__request('profile')

    def leaderboard(self, class_name=''):
        return self.__request('leaderboard', 'post', {'class_name': class_name})
    
    @staticmethod
    def ping():
        return requests.get(f'{WebCubers.base_url}ping')

    def __authenticate(self, username):
        response = self.__request('authenticate', 'post')
        return response

    def __request(self, endpoint, method='get', data={}):

        # Data
        data.update({
            'generated_at' : int(time.time())
        })
        data_query_string = urlencode(data)

        # Headers
        headers = {}
        headers['Username'] = self.api_username
        try:
            headers['Authorization'] = self.__sign_message(data_query_string, self.api_key)
        except:
            return {'status': False, 'code': 601, 'message': 'api key is malformed.'}
        
        headers.update(WebCubers.module_http_header) # Add module http header

        request_url = f'{WebCubers.base_url}{endpoint}'

        if method.lower() == 'get':
            response = requests.get(f'{request_url}?{data_query_string}', headers=headers)
        elif method.lower() == 'post':
            response = requests.post(request_url, data=data, headers=headers)
        
        if response.status_code == 481 or response.status_code == 403:
            return {'status': False, 'code': 481, 'message': 'FireEye Protection blocked your request, if you using any VPN, disconnect and try again.'}
    
        try:
            return response.json()
        except:
            return {'status': False, 'code': 600, 'message': 'connection error.'}

    def __sign_message(self, message, key):
        byte_key = binascii.unhexlify(key)
        message = message.encode()
        return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()
