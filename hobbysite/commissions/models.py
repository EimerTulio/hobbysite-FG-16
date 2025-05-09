from django.db import models
from django.urls import reverse

class Commission(models.Model):
    title = models.CharField(max_length = 225)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title
    
    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse('commissions:commissions-detail', args=[self.pk])

class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete = models.CASCADE, related_name = 'comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'Comment on {self.commission.title}'
    
    class Meta:
        ordering = ['-created_on']
