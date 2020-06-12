from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(User, models.Model):
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'user'


class SocialAuth(models.Model):
    user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, related_name='user')
    social_id = models.FloatField(unique=True)
    provider = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
