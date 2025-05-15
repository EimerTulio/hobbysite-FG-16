from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    search_fields = ('name',)
    list_display = ('name',)
    fieldsets = [
        (
            'Profile Information',
            {'fields': ['user', 'name', 'email']},
        ),
    ]


admin.site.register(Profile, ProfileAdmin)