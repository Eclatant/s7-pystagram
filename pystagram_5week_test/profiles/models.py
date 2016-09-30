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
