from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def set_firstname(self, firstname):
        self.first_name = firstname

    def set_lastname(self, lastname):
        self.last_name = lastname

    def get_fullname(self):
        return self.first_name + " " + self.last_name

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + "-" + str(self.pk)
        super(Assignment, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    message = models.TextField()
    isGeneral = models.BooleanField(default=False)
    usedNum = models.BigIntegerField(null=True)
    assignment = models.ForeignKey(Assignment)

    def add_count(self):
        if self.isGeneral:
            self.usedNum += 1

    def sub_count(self):
        if self.isGeneral and self.usedNum > 0:
            self.usedNum -= 1

    def set_message(self, message):
        self.message = message

    def __unicode__(self):
        return self.message


class FeedbackToStudent(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False)
    assignment = models.ForeignKey(Assignment, blank=False, null=False)
    comments = models.ForeignKey(Comment)

    def __unicode__(self):
        return self.student.student_id
