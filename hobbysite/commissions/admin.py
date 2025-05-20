from django.contrib import admin
from .models import Commission

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    """
    Handles the admin for commissions
    """

    list_display = ('title', 'people_required', 'created_on', 'updated_on')
    search_fields = ('title', 'description')
