from django.shortcuts import render, get_object_or_404, redirect
from .models import Commission, Comment, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm
from user_management.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def commission_list(request):
    commissions = list(Commission.objects.all())
    commissions.sort(key=lambda c: (c.status_order(), -c.created_on.timestamp()))

    user_commissions = []
    applied_commissions = []

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None

        user_commissions = Commission.objects.filter(author=profile).order_by('status', '-created_on')
        applied_commissions = Commission.objects.filter(jobs__applications__applicant=profile).distinct().order_by('status', '-created_on')
    
    else:
        user_commissions = []
        applied_commissions = []
    ctx = {
        'commissions': commissions,
        'user_commissions': user_commissions,
        'applied_commissions': applied_commissions,
    }
    return render(request, 'commission/commission_list.html', ctx)

def commission_detail(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id)
    comments = Comment.objects.filter(commission=commission).order_by('-created_on')
    jobs = commission.jobs.all()
    is_owner = request.user.profile == commission.author

    if request.method == 'POST':
        if 'apply_job' in request.POST:
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id)

            if job.get_open_slots() > 0:
                JobApplication.objects.create(
                    applicant=request.user.profile,
                    job=job,
                    status='Pending'
                )
                return redirect('commissions:commission_detail', commission_id=commission.id)

        elif is_owner and 'application_id' in request.POST:
            application_id = request.POST.get('application_id')
            application = get_object_or_404(JobApplication, id=application_id)

            if 'accept_application' in request.POST:
                if application.job.get_open_slots() > 0:
                    application.status = 'Accepted'
                    application.save()

            elif 'reject_application' in request.POST:
                application.status = 'Rejected'
                application.save()

            return redirect('commissions:commission_detail', commission_id=commission.id)

    applications = JobApplication.objects.filter(job__commission=commission)

    ctx = {
        'commission': commission,
        'jobs': jobs,
        'comments': comments,
        'is_owner': is_owner,
        'applications': applications,
    }

    return render(request, 'commission/commission_detail.html', ctx)

@login_required
def commission_create(request):
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.author = request.user.profile
            commission.save()
            return redirect('commissions:commission_list')
    else:
        form = CommissionForm()

    return render(request, 'commission/commission_add.html', {'form': form})
    
@login_required
def commission_update(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id)

    if commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=commission.id)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.created_on = commission.created_on
            commission.author = commission.author
            commission.save()
            
            if all(job.get_open_slots() == 0 for job in commission.jobs.all()):
                commission.status = 'Full'
                commission.save()

            return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = CommissionForm(instance=commission)

    return render(request, 'commission/commission_update.html', {
        'form': form,
        'commission': commission,
    })

@login_required
def job_create(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id)

    if commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=commission.id)
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.commission = commission
            job.save()
            return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = JobForm()

    return render(request, 'commission/job_form.html', {'form': form, 'commission': commission})

@login_required
def job_application_action(request, application_id, action):
    application = get_object_or_404(JobApplication, id=application_id)

    if application.job.commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=application.job.commission.id)

    if action == 'approve':
        application.status = 'Accepted'
    elif action == 'reject':
        application.status = 'Rejected'
    else:
        return redirect('commissions:commission_detail', commission_id=application.job.commission.id)

    application.save()

    if application.status == 'Accepted' and application.job.get_open_slots() == 0:
        application.job.status = 'Full'
        application.job.save()

    return redirect('commissions:commission_detail', commission_id=application.job.commission.id)

@login_required
def job_application(request, commission_id, job_id):
    commission = get_object_or_404(Commission, id=commission_id)
    jobs = commission.jobs.all()

    if job_id:
        job = get_object_or_404(Job, id=job_id)
    else:
        job = None

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_id = form.cleaned_data['job']
            job = get_object_or_404(Job, id=job_id)
            
            if job.commission.author == request.user.profile:
                form.add_error(None, 'You cannot apply to a job you created.')
                return render(request, 'commission/job_application_form.html', {'form': form, 'commission': commission, 'jobs': jobs})

            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user.profile
            application.save()

            return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = JobApplicationForm()

    return render(request, 'commission/job_application_form.html', {
        'form': form,
        'job': job,
        'commission': commission,
        'applications':JobApplication.objects.filter(job__commission=commission),
    })