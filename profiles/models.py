from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

#user_model_class = get_user_model()

from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL) # 매개변수는 문자열이고 그 이유는 전에 모델생성의 선행관계 방지용
    gender = models.CharField(max_length=1)
