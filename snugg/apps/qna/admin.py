from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import Answer, Comment, Field, Post


class FieldAdmin(DraggableMPTTAdmin):
    list_display = (
        "tree_actions",
        "indented_title",
    )

    list_display_links = ("indented_title",)

    mptt_level_indent = 20

    def indented_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield("level") * self.mptt_level_indent,
            instance.name,  # Or whatever you want to put here
        )


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "writer_link")

    list_display_links = (
        "pk",
        "title",
    )

    # readonly_fields = ('user_link',)

    def writer_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:user_user_change", args=(obj.writer.pk,)),
                obj.writer.email,
            )
        )

    writer_link.short_description = "writer"


# Register your models here.
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Field, FieldAdmin)
admin.site.register(Post, PostAdmin)
