from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField('글 본문', max_length=500)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(
        upload_to='%Y/%m/%d/', null=True, blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '글 번호: {}'.format(self.pk)

    def get_absolute_url(self):
        return '/photos/posts/{}/'.format(self.pk)

    class Meta:
        ordering = ('-created_at', '-pk', )


@receiver(post_delete, sender=Post)
def delete_attached_image(sender, instance, **kwargs):
    instance.image.delete(save=False)

#post_delete.connect(delete_attached_image, sender=Post)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)


