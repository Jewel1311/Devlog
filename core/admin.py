from django.contrib import admin
from .models import Profile, Tags, Posts, ReportCategory

admin.site.register(Profile)
admin.site.register(Tags)
admin.site.register(Posts)
admin.site.register(ReportCategory)
