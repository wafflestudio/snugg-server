from django.contrib import admin

from snugg.apps.agora.models import Lecture, Semester, Story

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Story)
admin.site.register(Semester)
