import re

from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.helper import register_user_with_social, register_user
from user.models import Profile, SocialAuth
from user.serializers import UserSerializer


@api_view(['POST'])
def register_new_user(request):
    try:
        profile = register_user(request)
        p = Profile.objects.get(username=profile.username)
        token = Token.objects.create(user=p)
        return Response({
            "result": 1,
            'token': token.key,
        })
    except Exception as e:
        print(e)
        return Response({
            "result": 0,
            "error": 'error'
        })


@api_view(['POST'])
def login(request):
    try:
        username = request.data['email']
        profile = Profile.objects.get(username=username)
        password = check_password(request.data['password'], profile.password)
        token = Token.objects.get(user=profile)
        if password:

            user_serializer = UserSerializer(profile)
            return Response({
                "user": user_serializer.data,
                "result": 1,
                'token': token.key,
            })
        else:
            return Response({
                "result": 0,
                "error": 'Incorrect Password'
            })

    except Exception as e:
        print(e)

        return Response({
            "result": 0,
            "error": 'Invalid Username'
        })


@api_view(['POST'])
def auth_social_view(request):
    try:
        social = SocialAuth.objects.get(provider=request.data['provider'], social_id=request.data['id'])
        profile = Profile.objects.get(pk=social.user.id)
        profile.last_login = timezone.now()
        profile.save()

        token = Token.objects.get(user=profile)
    except Exception:
        try:
            profile = Profile.objects.get(username=request.data['email'])
            profile.last_login = timezone.now()
            profile.save()
            register_user_with_social(request, profile)

            token = Token.objects.get(user=profile)
        except Profile.DoesNotExist:
            profile = register_user(request)
            register_user_with_social(request, profile)

            token = Token.objects.create(user=profile)

    return Response({
        'result': 1,
        'token': token.key,
        'user': UserSerializer(profile).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_page(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = re.search('.+ (.+)', token)
    user = Profile.objects.get(auth_token=token.group(1))

    return Response({
        'result': 1,
        "user": UserSerializer(user).data,
        "error": ''
    })
