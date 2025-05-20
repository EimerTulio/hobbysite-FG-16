from django import forms
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    """
    Form for creating or updating a Commission instance.
    """

    class Meta:
        model = Commission
        fields = ['title', 'description', 'people_required', 'status']


class JobForm(forms.ModelForm):
    """
    Form for creating a Job within a Commission, ensuring manpower validation.
    """

    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']
        widgets = {
            'status': forms.Select(choices=Job.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        self.commission = kwargs.pop('commission', None)
        super().__init__(*args, **kwargs)

    def clean_manpower_required(self):
        """
        Ensures total manpower of all jobs does not exceed commission's limit.
        """
        manpower = self.cleaned_data.get('manpower_required')
        if self.commission:
            existing_jobs = self.commission.jobs.exclude(
                id=self.instance.id if self.instance else None
            )
            total = sum(job.manpower_required for job in existing_jobs)
            if total + manpower > self.commission.people_required:
                raise forms.ValidationError(
                    f"Total manpower would exceed commission's limit of "
                    f"{self.commission.people_required}."
                )
        return manpower


class JobApplicationForm(forms.ModelForm):
    """
    Form for applying to a job under a specific commission.
    """
    job = forms.ModelChoiceField(queryset=Job.objects.none(), required=True)

    class Meta:
        model = JobApplication
        exclude = ['status', 'applicant']
        fields = ['job']

    def __init__(self, *args, **kwargs):
        commission = kwargs.get('commission')
        super().__init__(*args, **kwargs)
        if commission:
            self.fields['job'].queryset = commission.jobs.filter(status="Open")

    def save(self, commit=True):
        """
        Automatically set status to 'Accepted' upon saving.
        """
        instance = super().save(commit=False)
        instance.status = 'Accepted'
        if commit:
            instance.save()
        return instance


class JobUpdateForm(forms.ModelForm):
    """
    Form for updating a Job's manpower and status.
    """

    class Meta:
        model = Job
        fields = ['manpower_required', 'status']
        widgets = {
            'status': forms.Select(choices=Job.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_manpower_required(self):
        """
        Validates that manpower is not set below the number of accepted applications.
        """
        manpower_required = self.cleaned_data.get('manpower_required')
        if not self.instance:
            return manpower_required

        accepted = self.instance.accepted_applications()
        if manpower_required < accepted:
            raise forms.ValidationError(
                f"Manpower required cannot be less than the number of "
                f"accepted applications ({accepted})."
            )
        return manpower_required
