import hashlib
import requests
import hashlib
import hmac
import time
from collections import OrderedDict
from datetime import datetime
from lazada.validate import *

class Lazada:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://auth.lazada.com"
        self.base_url_rest = "https://auth.lazada.com/rest"
        self.base_url_th = "https://api.lazada.co.th/rest"
    
    def get_authorization_url(self, redirect_uri):
        return f"{self.base_url}/oauth/authorize?response_type=code&force_auth=true&redirect_uri={redirect_uri}&client_id={self.app_key}"
    
    def _sign(self, api_path, parameters):
        sort_dict = sorted(parameters)
        parameters_str = "%s%s" % (api_path,
            str().join('%s%s' % (key, parameters[key]) for key in sort_dict))   
        h = hmac.new(self.app_secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
        return h.hexdigest().upper()
    
    def get_access_token(self, authorization_code):
        path = "/auth/token/create"
        request_params = {
            'app_key': self.app_key,
            'code': authorization_code,
            'sign_method': 'sha256',
            'timestamp': int(round(time.time() * 1000)), 
        }
        signature = self._sign(path, request_params)
        request_params['sign'] = signature
        try:
            response = requests.post(
                url=f"{self.base_url_rest}{path}",
                params=request_params,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            print(f"Response Body: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def refresh_access_token(self, refresh_token):
        path = "/auth/token/refresh"
        request_params = {
            'app_key': self.app_key,
            'refresh_token': refresh_token,
            'sign_method': 'sha256',
            'timestamp': str(int(datetime.now().timestamp()) * 1000)
        }
        signature = self._sign(path, request_params)
        request_params['sign'] = signature
        try:
            response = requests.post(
                url=f"{self.base_url_rest}{path}",
                params=request_params,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            print(f"Response Body: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def _set_access_token(self, access_token):
        self.access_token = access_token
    
    def _set_commom_params(self, params:dict):
        common_params = {
            "app_key": self.app_key,
            "timestamp": str(int(time.time() * 1000)),
            "sign_method": "sha256",
            "access_token": self.access_token
        }
        common_params.update(params)
        return common_params
    
    def getDiscoveryReportCampaign(self, params:dict=None):
        if not hasattr(self, 'access_token'):
            raise Exception("Access token is not set. Please set the access token before making API calls.")
        
        params = self._set_commom_params(params or {})
        path = "/sponsor/solutions/report/getDiscoveryReportCampaign"
        request_params = DiscoveryReportParams(**params).model_dump(exclude_none=True)
        print(request_params)
        request_params['access_token'] = self.access_token
        
        print(request_params)
        signature = self._sign(path, request_params)
        request_params['sign'] = signature
        try:
            response = requests.post(
                url=f"{self.base_url_th}{path}",
                params=request_params,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            print(f"Response Body: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        