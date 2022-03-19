from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Answer, Comment, Field, Post


class FieldAdmin(DraggableMPTTAdmin):
    list_display = (
        "tree_actions",
        "indented_title",
    )


# Register your models here.
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Field, FieldAdmin)
admin.site.register(Post)
