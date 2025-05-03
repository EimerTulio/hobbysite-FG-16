from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Thread Category'
        verbose_name_plural = 'Thread Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum:post', args=[str(self.pk)])


class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        ThreadCategory,
        null=True,
        on_delete=models.SET_NULL,
        related_name="post_category",
    )
    entry = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True) 
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:post', args=[str(self.pk)])


class ThreadContent(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        Thread,
        null=False,
        on_delete=models.CASCADE,
        related_name="content",
    )

    def __str__(self):
        return self.content
    
class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    entry = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ['time_created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'