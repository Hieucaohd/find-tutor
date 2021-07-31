from google.oauth2 import id_token
from google.auth.transport import requests


class Google:

    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except:
            return "token khong hop le hoac da het han."
