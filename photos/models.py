from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_name = models.CharField(max_length=40)
    content = models.TextField(max_length=500)
    tags = models.ManyToManyField('Tag', blank=True)#blank 폼에서의 필수항목, null은 DB 널처리관련
    image = models.ImageField(
        upload_to='%Y/%m/%d/', null=True, blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = self.content[0:50]
        #return '{}. {}   #{}'.format(self.pk, title, self.tags.name)
        return '글 번호 : {}'.format(self.pk)

    class Meta:
        ordering = ('-created_at', '-pk',)

@receiver(post_delete, sender=Post)
def delete_attached_image(sender, instance, **kwargs):
    instance.image.delete(save=False)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey('Post')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey('Post')
    created_at = models.DateTimeField(auto_now_add=True)
