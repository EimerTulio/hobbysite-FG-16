from django.db import models
from django.urls import reverse
from user_management.models import Profile


class Commission(models.Model):
    """Model representing a commission."""

    STATUS_OPEN = 'Open'
    STATUS_FULL = 'Full'
    STATUS_COMPLETED = 'Completed'
    STATUS_DISCONTINUED = 'Discontinued'

    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_FULL, 'Full'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_DISCONTINUED, 'Discontinued'),
    ]

    STATUS_PRIORITY = {
        STATUS_OPEN: 0,
        STATUS_FULL: 1,
        STATUS_COMPLETED: 2,
        STATUS_DISCONTINUED: 3,
    }

    title = models.CharField(max_length=225)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='commissions', default=1
    )
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN
    )
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def status_order(self):
        """Return status priority for sorting."""
        return self.STATUS_PRIORITY.get(self.status, 99)

    def get_author(self):
        """Return the author of the commission."""
        return self.author

    def get_absolute_url(self):
        """Return the absolute URL to the commission detail view."""
        return reverse('commissions:commissions-detail', args=[self.pk])

    def total_manpower(self):
        """Return total manpower required for all jobs in the commission."""
        return sum(job.manpower_required for job in self.jobs.all())

    def total_open_manpower(self):
        """Return total remaining manpower (open slots) across all jobs."""
        return sum(
            job.manpower_required - job.accepted_applications()
            for job in self.jobs.all()
        )

    def update_status_if_full(self):
        """Update the commission status to full if all jobs are closed."""
        if all(job.status == Job.STATUS_CLOSED for job in self.jobs.all()):
            self.status = self.STATUS_FULL
            self.save()


class Job(models.Model):
    """Model representing a job under a commission."""

    OPEN = 'Open'
    CLOSED = 'Closed'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    commission = models.ForeignKey(
        Commission, related_name='jobs', on_delete=models.CASCADE
    )
    role = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=OPEN
    )
    manpower_required = models.PositiveIntegerField()

    def __str__(self):
        return self.role

    def get_open_slots(self):
        """Return the number of open slots for this job."""
        accepted_count = self.applications.filter(status='Accepted').count()
        return max(0, self.manpower_required - accepted_count)

    def accepted_applications(self):
        """Return the number of accepted applications for this job."""
        return self.applications.filter(status=JobApplication.STATUS_ACCEPTED).count()

    def update_status(self):
        """Update job status to closed if no slots are open, and delete pending apps."""
        if self.get_open_slots() <= 0:
            self.status = self.STATUS_CLOSED
            self.save()
            self.applications.filter(status=JobApplication.STATUS_PENDING).delete()


class JobApplication(models.Model):
    """Model representing a job application."""

    STATUS_PENDING = 'Pending'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications'
    )
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return f"{self.applicant} - {self.job.role} ({self.status})"
