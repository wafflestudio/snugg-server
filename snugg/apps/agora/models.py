from django.contrib.auth import get_user_model
from django.db import models

from snugg.apps.univ.models import College, Major, University

User = get_user_model()


class Lecture(models.Model):
    name = models.CharField(max_length=35)
    lecture_id = models.CharField(max_length=20)
    instructor = models.CharField(max_length=35)
    university = models.ForeignKey(
        University, related_name="lectures", on_delete=models.SET_NULL, null=True
    )
    college = models.ForeignKey(
        College, related_name="lectures", on_delete=models.SET_NULL, null=True
    )
    major = models.ForeignKey(
        Major, related_name="lectures", on_delete=models.SET_NULL, null=True
    )
    semesters = models.ManyToManyField("Semester", related_name="lectures")

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("lecture_id", "university"), name="unique_lecture"
            ),
        )


class Story(models.Model):
    lecture = models.ForeignKey(
        Lecture, related_name="storys", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        User, related_name="agora_storys", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Semester(models.Model):
    SEASON_CHOICES = (
        (1, "Winter"),
        (2, "Spring"),
        (3, "Summer"),
        (4, "Fall"),
    )

    year = models.IntegerField(default=2022)
    season = models.IntegerField(choices=SEASON_CHOICES, default=1)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("year", "season"), name="unique_semester"),
        )
        ordering = ("-year", "-season")

    def __str__(self):
        return f"{self.get_season_display()} {self.year}"
