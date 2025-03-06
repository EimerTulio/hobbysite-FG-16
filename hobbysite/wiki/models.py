from django.db import models
from django.urls import reverse

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return '{}: ArticleCategory'.format(self.name)
    
    def get_absolute_url(self):
        return reverse('article', args=[self.pk])
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        related_name="articles",
        null=True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    
    
