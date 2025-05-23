from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user_management.models import Profile
from .models import Commission, Job, JobApplication
from .forms import (
    CommissionForm, JobForm, JobApplicationForm, JobUpdateForm
)


@login_required
def commission_list(request):
    """
    Displays a list of all commissions, sorted by status and creation date.
    Shows user-created and applied commissions for authenticated users.
    """

    commissions = list(Commission.objects.all())
    commissions.sort(
        key=lambda c: (c.status_order(), -c.created_on.timestamp())
    )

    user_commissions = []
    applied_commissions = []

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None
        else:
            user_commissions = Commission.objects.filter(
                author=profile
            ).order_by('status', '-created_on')

            applied_commissions = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct().order_by('status', '-created_on')

    ctx = {
        'commissions': commissions,
        'user_commissions': user_commissions,
        'applied_commissions': applied_commissions,
    }

    return render(request, 'commission/commission_list.html', ctx)


@login_required
def commission_detail(request, commission_id):
    """
    Shows details of a commission with jobs and applications.
    Handles job applications and application approval/rejection.
    """

    commission = get_object_or_404(Commission, id=commission_id)
    jobs = commission.jobs.all()
    profile = request.user.profile
    is_owner = profile == commission.author

    if request.method == 'POST':
        if 'apply_job' in request.POST:
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id)
            already_applied = JobApplication.objects.filter(
                applicant=profile, job=job
            ).exists()

            if job.get_open_slots() > 0 and not already_applied:
                JobApplication.objects.create(
                    applicant=profile, job=job, status='Pending'
                )
                return redirect(
                    'commissions:commission_detail', commission_id=commission.id
                )

        elif is_owner and 'application_id' in request.POST:
            application_id = request.POST.get('application_id')
            application = get_object_or_404(JobApplication, id=application_id)

            if 'accept_application' in request.POST:
                if application.job.get_open_slots() > 0:
                    application.status = 'Accepted'
                    application.save()

                    job = application.job
                    if job.get_open_slots() <= 0:
                        job.status = Job.CLOSED
                        job.save()
                        job.applications.filter(status='Pending').delete()

                    commission = job.commission
                    if all(j.status == Job.CLOSED for j in commission.jobs.all()):
                        commission.status = 'Full'
                        commission.save()

            elif 'reject_application' in request.POST:
                application.status = 'Rejected'
                application.save()

            return redirect(
                'commissions:commission_detail', commission_id=commission.id
            )

    applications = JobApplication.objects.filter(job__commission=commission)

    ctx = {
        'commission': commission,
        'jobs': jobs,
        'is_owner': is_owner,
        'applications': applications,
    }

    return render(request, 'commission/commission_detail.html', ctx)


@login_required
def commission_create(request):
    """
    Allows logged-in users to create a new commission.
    Sets the current user as the commission author.
    """

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
    """
    Allows commission owners to edit commission details.
    """

    commission = get_object_or_404(Commission, id=commission_id)

    if commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=commission.id)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.created_on = commission.created_on
            commission.author = commission.author
            form.save()

            if all(job.get_open_slots() == 0 for job in commission.jobs.all()):
                commission.status = 'Full'
                commission.save()

            return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = CommissionForm(instance=commission)

    ctx = {
        'form': form,
        'commission': commission,
    }

    return render(request, 'commission/commission_update.html', ctx)


@login_required
def job_create(request, commission_id):
    """
    Allows commission owners to add new jobs within manpower limits.
    """

    commission = get_object_or_404(Commission, id=commission_id)

    if commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=commission.id)

    if request.method == 'POST':
        form = JobForm(request.POST, commission=commission)
        if form.is_valid():
            new_job = form.save(commit=False)

            current_total = sum(
                job.manpower_required for job in commission.jobs.all())
            proposed_total = current_total + new_job.manpower_required

            if proposed_total > commission.people_required:
                form.add_error(
                    'manpower_required', f"Total manpower exceeds the required number of {commission.people_required}.")
            else:
                new_job.commission = commission
                new_job.save()
                return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = JobForm(commission=commission)

    ctx = {
        'form': form,
        'commission': commission
        }
    return render(request, 'commission/job_form.html', ctx)


@login_required
def job_application_action(request, application_id, action):
    """
    Allows commission owners to approve or reject applications.
    """

    application = get_object_or_404(JobApplication, id=application_id)
    profile = request.user.profile

    if application.job.commission.author != profile:
        return redirect(
            'commissions:commission_detail',
            commission_id=application.job.commission.id
        )

    if action == 'approve':
        application.status = 'Accepted'
        accepted_count = application.job.applications.filter(status='Accepted').count()
        if accepted_count >= application.job.manpower_required:
            application.job.status = Job.CLOSED
            application.job.save()
    elif action == 'reject':
        application.status = 'Rejected'
    else:
        return redirect(
            'commissions:commission_detail',
            commission_id=application.job.commission.id
        )

    application.save()

    return redirect(
        'commissions:commission_detail',
        commission_id=application.job.commission.id
    )


@login_required
def job_application(request, commission_id, job_id):  
    """
    Handles job application submissions from users.
    Prevents commission owners from applying to their own jobs.
    """
    commission = get_object_or_404(Commission, id=commission_id)
    job = get_object_or_404(Job, id=job_id, commission=commission)

    if job.commission.author == request.user.profile:
        return render(request, 'commission/job_application_form.html', {
            'error': 'You cannot apply to a job you created.',
            'commission': commission,
            'job': job,
        })

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            already_applied = JobApplication.objects.filter(
                applicant=request.user.profile,
                job=job
            ).exists()

            if already_applied:
                form.add_error(None, 'You have already applied to this job.')
            elif job.get_open_slots() <= 0:
                form.add_error(None, 'This job is full.')
            else:
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user.profile
                application.status = 'Pending'
                application.save()
                return redirect('commissions:commission_detail', commission_id=commission.id)
    else:
        form = JobApplicationForm()

    ctx = {
        'form': form,
        'commission': commission,
        'job': job,
    }

    return render(request, 'commission/job_application_form.html', ctx)


@login_required
def job_update(request, commission_id):
    """
    Allows commission owners to update their jobs while respecting manpower limits.
    """
    commission = get_object_or_404(Commission, id=commission_id)

    if commission.author != request.user.profile:
        return redirect('commissions:commission_detail', commission_id=commission.id)

    jobs = commission.jobs.all()
    selected_job = None
    form = None

    if request.method == 'POST':
        job_id = request.POST.get('job_select') or request.POST.get('job_id')

        if job_id:
            selected_job = get_object_or_404(Job, id=job_id, commission=commission)

        if 'update_job' in request.POST and selected_job:
            form = JobUpdateForm(request.POST, instance=selected_job)
            if form.is_valid():
                updated_job = form.save(commit=False)
                total_manpower_except_current = sum(
                    j.manpower_required for j in commission.jobs.exclude(pk=selected_job.pk)
                )
                proposed_total = total_manpower_except_current + updated_job.manpower_required

                if proposed_total > commission.people_required:
                    form.add_error(
                        'manpower_required',
                        f'Total manpower ({proposed_total}) exceeds commission limit of {commission.people_required}.'
                    )
                else:
                    updated_job.save()

                    if all(j.status == Job.CLOSED for j in commission.jobs.all()):
                        commission.status = 'Full'
                        commission.save()

                    return redirect('commissions:commission_detail', commission_id=commission.id)

        elif selected_job:
            form = JobUpdateForm(instance=selected_job)

    ctx = {
        'commission': commission,
        'jobs': jobs,
        'selected_job': selected_job,
        'form': form,
    }

    return render(request, 'commission/job_update.html', ctx)
