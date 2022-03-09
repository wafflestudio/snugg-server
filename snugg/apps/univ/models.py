from django.db import models

from snugg.apps.user.models import User


class UnivProfile(models.Model):
    UNDERGRADUATE = "U"
    ASSOCIATE = "A"
    BACHELOR = "B"
    MASTER = "M"
    DOCTOR = "D"
    DEGREE_CHOICES = [
        (UNDERGRADUATE, "undergraduate"),
        (ASSOCIATE, "associate"),
        (BACHELOR, "bachelor"),
        (MASTER, "master"),
        (DOCTOR, "doctor"),
    ]
    user = models.ForeignKey(User, related_name="profiles", on_delete=models.CASCADE)
    university = models.ForeignKey(
        "University", related_name="profiles", on_delete=models.SET_NULL, null=True
    )
    college = models.ForeignKey(
        "College", related_name="profiles", on_delete=models.SET_NULL, null=True
    )
    major = models.ForeignKey(
        "Major", related_name="profiles", on_delete=models.SET_NULL, null=True
    )
    admission_year = models.IntegerField(null=True)
    graduated = models.BooleanField(null=True)
    degree = models.CharField(max_length=1, choices=DEGREE_CHOICES, blank=True)
    email = models.EmailField(unique=False)


class University(models.Model):
    members = models.ManyToManyField(User, through="UnivProfile")
    name = models.CharField(max_length=20)
    email_host = models.CharField(blank=True, max_length=30)
    logo_image = models.ImageField(null=True)


class College(models.Model):
    university = models.ForeignKey(
        University, related_name="colleges", on_delete=models.CASCADE
    )
    name = models.CharField(blank=True, max_length=30)


class Major(models.Model):
    university = models.ForeignKey(
        University, related_name="majors", on_delete=models.CASCADE
    )
    college = models.ForeignKey(
        College, related_name="majors", on_delete=models.CASCADE
    )
    name = models.CharField(blank=True, max_length=30)
