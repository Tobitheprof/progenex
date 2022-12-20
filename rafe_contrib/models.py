from django.db import models
from django.contrib.auth import get_user_model

RafeUser = get_user_model()


class rafe_contrib_Profile(models.Model):
    owner = models.ForeignKey(RafeUser, on_delete=models.SET_NULL, null=True)
    user_id = models.IntegerField()
    address = models.CharField(max_length=400)
    occupation = models.CharField(max_length=300)
    profile_img = models.FileField(upload_to="rafe_contrib_Pics")
    twitter_link = models.CharField(max_length=300, blank=True, null=True)
    linkedin_link = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=300)
    about_me = models.TextField()

    def __str__(self):
        return self.owner.username


class rafe_contrib_Work(models.Model):
    owner = models.ForeignKey(RafeUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    org_name = models.CharField(max_length=300)
    start = models.IntegerField()
    stop = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title


class rafe_contrib_Skill(models.Model):
    owner = models.ForeignKey(RafeUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    proficiency = models.IntegerField()

    def __str__(self):
        return self.name


class rafe_contrib_Education(models.Model):
    owner = models.ForeignKey(RafeUser, on_delete=models.SET_NULL, null=True)
    institution = models.CharField(max_length=300)
    degree = models.CharField(max_length=300)
    course_of_study = models.CharField(max_length=300)
    start = models.CharField(max_length=300)
    stop = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.institution


class rafe_contrib_Achievements(models.Model):
    owner = models.ForeignKey(RafeUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title
