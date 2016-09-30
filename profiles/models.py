from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#from django.contrib.auth import get_user_model

#user_model_class = get_user_model()

class Profile(models.Model):
    #user = models.OneToOneField(user_model_class)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1)
