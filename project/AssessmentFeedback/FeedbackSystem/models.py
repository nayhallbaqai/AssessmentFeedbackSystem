from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    courses = models.ManyToMany(Course)

class Course(models.Model):
    name = models.CharField(max_length=50)
    tutors = models.ManyToMany(Staff)

class Assignment(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course)


class Comment(models.Model):

