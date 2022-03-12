from django.contrib import admin

from .models import College, Major, University, UnivProfile

# Register your models here.
admin.site.register(College)
admin.site.register(Major)
admin.site.register(University)
admin.site.register(UnivProfile)
