from django.db import models


class University(models.Model):
    # members = models.ManyToManyField('User', through='UnivProfile')
    name = models.CharField(max_length=20)
    email_host = models.CharField(blank=True, max_length=30)
    # logo_image = models.ImageField(upload_to='')


class College(models.Model):
    university = models.ForeignKey(University, related_name='colleges', on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=30)


class Major(models.Model):
    university = models.ForeignKey(University, related_name='majors', on_delete=models.CASCADE)
    college = models.ForeignKey(College, related_name='majors', on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=30)