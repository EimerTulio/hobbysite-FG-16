from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ArticleCategory(models.Model):
    '''ArticleCategory model for wiki articles'''
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return '{}: ArticleCategory'.format(self.name)
    
    def get_absolute_url(self):
        return reverse('wiki:article-list')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

class Article(models.Model):
    '''Article model for wiki articles'''
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="articles",
        null=True,
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        related_name="articles",
        null=True,
    )
    entry = models.TextField()
    header_image = models.ImageField(upload_to='article_headers/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{}: Article'.format(self.title)
    
    def get_absolute_url(self):
        return reverse('wiki:article-detail', args=[self.pk])
    
    class Meta:
        ordering = ['-created_on']
        
class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}: Comment'.format(self.title)
    
    class Meta:
        ordering = ['-created_on']
