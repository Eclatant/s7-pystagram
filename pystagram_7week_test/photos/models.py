from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(
                upload_to='%Y/%m/%d/', null=True, blank=True,
            )

    #모델에 직접 delete함수를 오버라이딩하여 이미지 삭제를 적용할 수 있다.
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)

@receiver(post_delete, sender=Photo)
def delete_attached_image(sender, instance, **kwargs):
    instance.image.delete(save=False)
    # DB에서 지워져도 파이썬 객체로 Photo모델이 남아있기 때문에 접근가능

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

"""
selection field가 있는 경우

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    selection = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)
"""

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)
