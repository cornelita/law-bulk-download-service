import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

API_AUTH_URL = 'http://34.168.241.7'


class KamiRandomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Missing Authorization token')

        user = requests.get(url=f'{API_AUTH_URL}/api/user/', headers={
            'Authorization': token
        })
        if user.status_code != 200:
            raise AuthenticationFailed('Invalid token.')

        return (user.json(), None)

    def authenticate_header(self, request):
        return 'Token'
