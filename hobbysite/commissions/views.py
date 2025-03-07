from django.shortcuts import render
from .models import Commission, Comment

def commission_list(request):
    commissions = Commission.objects.all().order_by('-created_on')
    ctx = {
        'commissions': commissions
    }
    return render(request, 'commission.html', ctx)

def commission_detail(request, commission_id):
    commission = Commission.objects.get(id = commission_id)
    comments = Comment.objects.filter(commission = commission).order_by('-created_on')
    ctx = {
        'commission': commission,
        'comments': comments,
    }
    return render(request, 'commission_detail.html', ctx)