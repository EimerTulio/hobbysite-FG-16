from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ArticleCategory(models.Model):
    '''ArticleCategory model for wiki articles'''
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return '{}'.format(self.name)
    
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
        related_name="article_author",
        null=True,
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        related_name="article_category",
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
    '''Comment model for wiki articles'''
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="comment_author",
        null=True,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comment_article"
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}: Comment'.format(self.author.user.username)

    class Meta:
        ordering = ['-created_on']

class ArticleImage(models.Model):
    '''ArticleImage model for wiki articles'''
    image = models.ImageField(null=True, upload_to='article_images/')
    description = models.CharField(max_length=255)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="images"
    )
