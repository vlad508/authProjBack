from rest_framework import serializers

from user.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email')
