from django import forms
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'people_required', 'status']


class JobForm(forms.ModelForm):
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
        manpower = self.cleaned_data.get('manpower_required')
        if self.commission:
            existing_jobs = self.commission.jobs.exclude(
                id=self.instance.id if self.instance else None)
            total_existing = sum(
                job.manpower_required for job in existing_jobs)
            if total_existing + manpower > self.commission.people_required:
                raise forms.ValidationError(
                    f"Total manpower would exceed the commission's requirement of {self.commission.people_required}."
                )
        return manpower


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['status', 'applicant', 'job']
        fields = ['job']

    job = forms.ModelChoiceField(queryset=Job.objects.none(), required=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'Accepted'
        if commit:
            instance.save()
        return instance
    def __init__(self, *args, **kwargs):
        commission = kwargs.get('commission')
        super().__init__(*args, **kwargs)
        if commission:
            self.fields['job'].queryset = commission.jobs.filter(status="Open")


class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['manpower_required', 'status']
        widgets = {
            'status': forms.Select(choices=Job.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        self.job_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
    def clean_manpower_required(self):
        manpower_required = self.cleaned_data.get('manpower_required')
        if not self.instance:
            return manpower_required

        accepted = self.instance.accepted_applications()

        if manpower_required < accepted:
            raise forms.ValidationError(
                f"Manpower required cannot be less than the number of accepted applications ({accepted})."
            )
        return manpower_required
