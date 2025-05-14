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