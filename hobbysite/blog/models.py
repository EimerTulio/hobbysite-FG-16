from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    
    description = models.TextField()

    class Meta:
        ordering = ['name'] 
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return self.name



class Article (models.Model):
    title = models.CharField(max_length=255) 
    category = models.ForeignKey(ArticleCategory, null=True, on_delete=models.SET_NULL)
    entry = models.TextField()

    created_on = models.DateTimeField(auto_now_add = True)
    last_updated = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.pk])