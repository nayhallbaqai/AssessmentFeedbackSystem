from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.student_id

class Course(models.Model):
    name = models.CharField(max_length=50)
    tutors = models.ManyToManyField(User)
    class_list = models.ManyToManyField(Student)

    def __unicode__(self):
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    message = models.TextField()
    isGeneral = models.BooleanField(default=False)
    usedNum = models.BigIntegerField()
    assignment = models.ForeignKey(Assignment)

    def __unicode__(self):
        return self.message

class FeedbackToStudent(models.Model):
    student = models.ForeignKey(Student, blank=False ,null=False)
    assignment = models.ForeignKey(Assignment, blank=False, null=False)
    comments = models.ForeignKey(Comment, blank=True, null=True)

    def __unicode__(self):
        return self.student.student_id