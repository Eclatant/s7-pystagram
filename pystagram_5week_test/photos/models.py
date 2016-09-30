from django.db import models
from django.conf import settings

class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)

class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)
