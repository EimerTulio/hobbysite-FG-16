from django.urls import path
from .views import commission_list, commission_detail, commission_create, commission_update, job_application, job_create, job_update

urlpatterns = [
    path('list/', commission_list, name = 'commission_list'),
    path('<int:commission_id>/', commission_detail, name = 'commission_detail'),
    path('add/', commission_create, name='commission_create'),
    path('<int:commission_id>/update/', commission_update, name = 'commission_update'),
    path('<int:commission_id>/edit/', commission_update, name='commission_edit'),
    path('<int:commission_id>/jobs/<int:job_id>/apply/', job_application, name='job_application_form'),
    path('<int:commission_id>/jobs/create/', job_create, name='job_form'),
    path('<int:commission_id>/jobs/update/', job_update, name = 'job_update'),
]

app_name = "commissions"
