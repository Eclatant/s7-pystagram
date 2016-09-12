from django.db import models

class Post(models.Model):
    content = models.TextField(max_length=500)
    tags = models.ManyToManyField('Tag', blank=True)#blank 폼에서의 필수항목, null은 DB 널처리관련
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = self.content[0:50]
        #return '{}. {}   #{}'.format(self.pk, title, self.tags.name)
        return '글 번호 : {}'.format(self.pk)

    class Meta:
        ordering = ('-created_at', '-pk',)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
