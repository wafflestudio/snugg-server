from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

User = get_user_model()
choice_limit = models.Q(model="Post") | models.Q(model="Answer")


class Field(MPTTModel):
    name = models.CharField(max_length=20)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


class Answer(models.Model):
    post = models.ForeignKey("Post", null=True, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    comments = GenericRelation("Comment", related_query_name="answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=choice_limit, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    field = TreeForeignKey("Field", null=True, blank=True, on_delete=models.SET_NULL)
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_answer = models.OneToOneField(
        "Answer", null=True, on_delete=models.CASCADE, related_name="bulletin"
    )
    comments = GenericRelation("Comment", related_query_name="post")
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        """
        If this Post object is not created yet,
        or the accepted answer's 'post' field does not point to this object,
        the accepted answer is forced to be None.
        """
        if self.pk is None or (
            self.accepted_answer and self.accepted_answer.post != self
        ):
            self.accepted_answer = None

        super().save(*args, **kwargs)


# class Tag(models.Model):
#     posts = models.ManyToManyField("Post")
#     name = models.CharField(max_length=30)
