from django.db import models
from django.urls import reverse
from user_management.models import Profile

class Commission(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]

    STATUS_PRIORITY = {
    'Open': 0,
    'Full': 1,
    'Completed': 2,
    'Discontinued': 3,
    }

    title = models.CharField(max_length = 225)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='commissions', default = 1)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def status_order(self):
        return self.STATUS_PRIORITY.get(self.status, 99)
    
    class Meta:
        ordering = ['-created_on']
        
    def get_author(self):
        return self.author

    def get_absolute_url(self):
        return reverse('commissions:commissions-detail', args=[self.pk])
    
    def total_manpower(self):
        return sum(job.manpower_required for job in self.jobs.all())

    def total_open_manpower(self):
        return sum(job.manpower_required - job.accepted_applications() for job in self.jobs.all())
    
    def update_status_if_full(self):
        if all(job.status == Job.CLOSED for job in self.jobs.all()):
            self.status = 'Full'
            self.save()

class Job(models.Model):
    OPEN = 'Open'
    CLOSED = 'Closed'
    
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]
    
    commission = models.ForeignKey(Commission, related_name="jobs", on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN)
    manpower_required = models.PositiveIntegerField()

    def get_open_slots(self):
        accepted_applications_count = JobApplication.objects.filter(job=self, status='Accepted').count()
        return self.manpower_required - accepted_applications_count

    def __str__(self):
        return self.role
    
    def accepted_applications(self):
        return self.applications.filter(status='Accepted').count()
    
    def update_status(self):
        if self.get_open_slots() <= 0:
            self.status = self.CLOSED
            self.save()
            self.applications.filter(status='Pending').delete()
    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on'] 

    def __str__(self):
        return f"{self.applicant} - {self.job.role} ({self.status})"

class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete = models.CASCADE, related_name = 'comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'Comment on {self.commission.title}'
    
    class Meta:
        ordering = ['-created_on']
