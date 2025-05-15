from django.db import models
from django.urls import reverse

from user_management.models import Profile


class ThreadCategory(models.Model):
    """A model representing a category for a Thread."""
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Thread Category'
        verbose_name_plural = 'Thread Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url for this Thread Category."""
        return reverse('forum:post', args=[str(self.pk)])


class Thread(models.Model):
    """A model representing a forum Thread."""
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="thread")
    category = models.ForeignKey(
        ThreadCategory,
        null=True,
        on_delete=models.SET_NULL,
        related_name="post_category",
    )
    entry = models.TextField()
    image = models.ImageField(upload_to="forum/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url for this Thread."""
        return reverse('forum:post', args=[str(self.pk)])


class ThreadContent(models.Model):
    """A model representing the text content of a forum Thread."""
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
    """A model representing a comment by a user on a forum Thread."""
    author = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="thread_comment")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    entry = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['time_created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
