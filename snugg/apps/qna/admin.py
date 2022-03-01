from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Field


class FieldAdmin(DraggableMPTTAdmin):
    list_display = (
        "tree_actions",
        "indented_title",
    )


admin.site.register(Field, FieldAdmin)


# Register your models here.
