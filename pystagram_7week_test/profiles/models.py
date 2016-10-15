from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

#user_model_class = get_user_model()

from django.conf import settings

class Profile(models.Model):
    #user = models.OneToOneField(User) # User모델 직접 import함
    #user = models.OneToOneField(user_model_class) # settings를 통해서 하는 것이 더 일반적임
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return '글 번호 : {}'.format(self.pk)

class FollowList(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    follow = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)
