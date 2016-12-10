from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext

from FeedbackSystem.models import Student, Course, Assignment, Comment, FeedbackToStudent


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('course/')

    return HttpResponseRedirect('/accounts/login/')


@login_required
def course(request):
    context = {}
    courses = []
    allAssignment = []
    if request.method == 'GET':
        courses = getUserCourses(request.user)
        allAssignment = getUserAllAssignment(request.user)

    context['user'] = request.user
    context['courses'] = courses
    context['AllAssignments'] = allAssignment
    return render(request, 'FeedbackSystem/courseAssignment.html', context)


def getUserCourses(user):
    courses = []
    if user.is_authenticated():
        courses = user.course_set.all()
    return courses


def getAssignmentsByCourse(course):
    if Course.objects.filter(pk=course.pk).exists():
        return course.assignment_set.all()
    else:
        return []


def getUserAllAssignment(user):
    allAssignment = []
    courses = getUserCourses(user)
    for course in courses:
        assignment = getAssignmentsByCourse(course)
        allAssignment += assignment

    return allAssignment


def getCourseByID(id):
    if Course.objects.filter(pk=id).exists():
        return Course.objects.get(pk=id)
    else:
        return None


@login_required
def getAssignments(request):
    context = {}
    assignment = []
    if request.method == "POST":
        course_id = request.POST['id']
        if course_id == "All":
            assignment = getUserAllAssignment(request.user)
        else:
            courseObject = getCourseByID(course_id)
            if courseObject == None:
                return render(request, 'FeedbackSystem/assignment.html', context)
            else:
                assignment = getAssignmentsByCourse(courseObject)

        context['assignments'] = assignment
        return render(request, 'FeedbackSystem/assignment.html', context)
    else:
        return render(request, 'FeedbackSystem/assignment.html', context)

# def addAssignment(request):
#     context = {}
#
#     return render(request, 'FeedbackSystem/addedAssignment.html', context)