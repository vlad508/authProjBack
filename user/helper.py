import secrets
import string

from django.contrib.auth.hashers import make_password
from django.utils import timezone

from user.models import SocialAuth, Profile


def random_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))

    return password


def register_user(request):
    profile = Profile()
    profile.email = request.data['email']
    profile.username = request.data['email']
    if request.data.get('password') is not None:
        profile.password = make_password(request.data['password'])
    profile.first_name = request.data.get('first_name', '')
    profile.last_name = request.data.get('last_name', '')
    profile.last_login = timezone.now()

    if profile.first_name == '' and profile.last_name == '':
        profile.first_name = request.data['firstName']
        profile.last_name = request.data['lastName']
        profile.password = make_password(random_password())

    profile.save()
    return profile


def register_user_with_social(request, profile):
    social = SocialAuth()
    social.social_id = request.data['id']
    social.provider = request.data['provider']
    social.user = profile
    social.save()
