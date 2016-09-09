from django.db import models
from django.db.models import Q

# Create your models here.

class BaseFormat(models.Model):
	userid = models.CharField(max_length=15)
	content = models.TextField(max_length=6000)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '글 번호: {}'.format(self.pk)

	class Meta:
		abstract = True

class Post(BaseFormat):
	title = models.CharField(max_length=100)
	filepath = models.CharField(max_length=255)

	class Meta:
		ordering = ('-created_at', '-pk')

class Comment(BaseFormat):
	post = models.ForeignKey('Post')

class Tag(models.Model):
	post = models.ManyToManyField('Post')
	tagname = models.CharField(max_length=20)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)