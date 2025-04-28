from django.contrib import admin
from .models import ThreadCategory, Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    search_fields = ('name',)
    list_display = ('name',)
    fieldsets = [
        (
            'Thread Category Information',
            {'fields': ['name', 'description']},
        ),
    ]


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    search_fields = ('title',)
    list_display = ('title', 'time_created')
    fieldsets = [
        (
            'Threads Information',
            {'fields': ['title', 'entry', 'category']},
        ),
    ]


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)