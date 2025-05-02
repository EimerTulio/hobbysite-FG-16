from django.db import models
from django.urls import reverse


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum:post', args=[str(self.pk)])


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        PostCategory,
        null=True,
        on_delete=models.SET_NULL,
        related_name="post_category",
    )
    entry = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)  # Only sets the time when it's created
    time_updated = models.DateTimeField(auto_now=True)  # Updates timestamp every time the object is saved

    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:post', args=[str(self.pk)])


class PostContent(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        Post,
        null=False,
        on_delete=models.CASCADE,
        related_name="content",
    )

    def __str__(self):
        return self.content