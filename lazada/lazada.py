import hashlib
import requests
import hashlib
import hmac
import time
from collections import OrderedDict

class Lazada:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://auth.lazada.com"
    
    def get_authorization_url(self, redirect_uri):
        return f"{self.base_url}/oauth/authorize?response_type=code&force_auth=true&redirect_uri={redirect_uri}&client_id={self.app_key}"
    
    def _sign(self, api_path, parameters):
        sort_dict = sorted(parameters)
        parameters_str = "%s%s" % (api_path,
            str().join('%s%s' % (key, parameters[key]) for key in sort_dict))
        print(parameters_str)       
        h = hmac.new(self.app_secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
        return h.hexdigest().upper()
    
    def get_access_token(self, authorization_code):
        path = "/rest/auth/token/create"
        request_params = {
            'app_key': self.app_key,
            'code': authorization_code,
            'sign_method': 'sha256',
            'timestamp': int(round(time.time() * 1000)), 
        }
        signature = self._sign(path, request_params, self.app_secret)
        request_params['sign'] = signature
        try:
            response = requests.post(
                url=f"{self.base_url}{path}",
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