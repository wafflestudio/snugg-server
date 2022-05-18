from django.contrib import admin

from snugg.apps.agora.models import Lecture, Post, Semester

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Post)
admin.site.register(Semester)
