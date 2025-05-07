from django.shortcuts import render, get_object_or_404
from .models import Commission, Comment

def commission_list(request):
    commissions = Commission.objects.all().order_by('-created_on')
    ctx = {
        'commissions': commissions
    }
    return render(request, 'commission/commission_list.html', ctx)

def commission_detail(request, commission_id):
    commission = get_object_or_404(Commission, id=commission_id)
    comments = Comment.objects.filter(commission=commission).order_by('-created_on')
    ctx = {
        'commission': commission,
        'comments': comments,
    }
    return render(request, 'commission/commission_detail.html', ctx)