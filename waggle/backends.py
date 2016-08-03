from django.contrib.auth.models import User
from oauth2client import client, crypt
from django.http import HttpResponse
from django.conf import settings

class GoogleAuthBackend(object):
    def authenticate(self, token=None):
        try:
            idinfo = client.verify_id_token(token, settings.CLIENT_ID)
            # If multiple clients access the backend server:
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
                return None
            '''
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['hd'] != APPS_DOMAIN_NAME:
                raise crypt.AppIdentityError("Wrong hosted domain.")
            '''
        except crypt.AppIdentityError:
            # Invalid token
            raise crypt.AppIdentityError("Invalid token.")
            return None
        userid = idinfo['sub']

        try:
            user = User.objects.get(username=userid)
        except User.DoesNotExist:
            user = User(username=userid, email=idinfo['email']) 
            user.set_unusable_password()
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
