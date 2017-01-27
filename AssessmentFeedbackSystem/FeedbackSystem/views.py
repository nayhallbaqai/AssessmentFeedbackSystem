import StringIO
import os
import tempfile
import zipfile
import json

from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.http import JsonResponse

from FeedbackSystem.models import Student, Course, Assignment, Comment, FeedbackToStudent


# Create your views here.
# from AssessmentFeedbackSystem.FeedbackSystem.forms import AddAssignmentForm


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

@login_required
def get_user_courses(request):
    context = {}
    if request.method == "POST":
        try:
            staff = request.user
            forMainContent = json.loads(request.POST['forMainContent'])
        except KeyError:
            return HttpResponse('forManContent boolean not specified')

        context['forMainContent'] = forMainContent

        courses = getUserCourses(staff)
        if course is not []:
            context['courses'] = courses

        return render(request, 'FeedbackSystem/getCourses.html', context)
    else:
        return HttpResponse('Not a POST request')

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
def add_course(request):
    if request.method == "POST":
        try:
            staff = request.user
            course_title = request.POST['name']
        except KeyError:
            return HttpResponse('you must specify course name')

        course = Course.objects.create(name=course_title)

        course.tutors.add(staff)
        course.save()

        return HttpResponse('course is added')

    else:
        return HttpResponse('Not a POST request')

@login_required
def delete_course(request):
    if request.method == "POST":

        try:
            staff = request.user
            course_id = request.POST['course_id']
        except KeyError:
            return HttpResponse('you must select a course')

        course = getCourseByID(course_id)

        if course is None:
            return HttpResponse('Not a valid course_id')

        if not course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('Course cannot be deleted')

        # if more than one tutor
        if course.tutors.all().count() > 1:
            staff.course_set.remove(course)
            staff.save()
        else:
            course.delete()

        return HttpResponse('Course deleted successfully')

    else:
        return HttpResponse('Not a POST request')

@login_required
def course_assignment_to_tutor(request):
    if request.method == "POST":
        try:
            staff = request.user
            courses = request.POST.getlist('courses[]')
            username = request.POST['username']
        except KeyError:
            return HttpResponse('you must select a course and enter a tutors name')

        if len(courses) == 0:
            return HttpResponse('please select a course')

        try:
            tutor = User.objects.get(username=username)
        except User.DoesNotExists:
            return HttpResponse('Please enter the right username')

        for course_id in courses:
            if staff.course_set.filter(pk=course_id).exists():
                course = getCourseByID(course_id)
                tutor.course_set.add(course)

        tutor.save()

        return HttpResponse(username + ' is assigned to the selected courses')

    else:
        return HttpResponse('Not a POST request')

@login_required
def get_assignments(request):
    context = {}
    if request.method == "POST":
        course_id = request.POST['id']
        if course_id == "All":
            assignment = getUserAllAssignment(request.user)
        else:
            courseObject = getCourseByID(course_id)
            if courseObject is None:
                return render(request, 'FeedbackSystem/assignment.html', context)
            else:
                assignment = getAssignmentsByCourse(courseObject)

        context['assignments'] = assignment
        return render(request, 'FeedbackSystem/assignment.html', context)
    else:
        return render(request, 'FeedbackSystem/assignment.html', context)


@login_required
def add_assignment(request):
    context = {}
    assignmentAdded = False
    if request.method == "POST":
        try:
            title = request.POST['title']
            course_id = request.POST['course_id']
        except KeyError:
            return HttpResponse('you must specify title or course id')

        course_by_id = getCourseByID(course_id)
        if course_by_id is not None:
            assignment, created = Assignment.objects.get_or_create(title=title, course=course_by_id)
            if created:
                assignment.save()
                assignmentAdded = True
    context['assignmentAdded'] = assignmentAdded
    return render(request, 'FeedbackSystem/addAssignment.html', context)


@login_required
def get_all_student(request):
    context = {}
    if request.method == "GET":
        try:
            students = Student.objects.all()
            context['students'] = students
        except Student.DoesNotExist:
            context['students'] = []

    return render(request, 'FeedbackSystem/studentTable.html', context)


'''
-------------------------------------------------------------------------------------------------
-------------------------- Code Section for Live Student Table ----------------------------------
-------------------------------------------------------------------------------------------------
'''


@login_required
def get_course_class_list(request):
    context = {}
    if request.method == "POST":
        try:
            staff = request.user
            courseID = request.POST['course_id']
        except KeyError:
            return HttpResponse("CourseID is not specified")

        try:
            if staff.course_set.filter(pk=courseID).exists():
                courseObject = getCourseByID(courseID)
                students = courseObject.class_list.all()
                context['students'] = students
                tutor = True
            else:
                tutor = False

            context['tutor'] = tutor
            return render(request, 'FeedbackSystem/studentTable.html', context)

        except ValueError:
            return HttpResponse("Course ID can not be filtered")

    else:
        return HttpResponse("Not a POST request")


@login_required
def add_students(request):
    if request.method == "POST":
        try:
            id = request.POST['student_id']
            first_name = request.POST.get('first_name', "")
            last_name = request.POST.get('last_name', "")
            courseID = request.POST['course_id']
        except KeyError:
            return HttpResponse("You must specify student_id and course id")

        if not course_exists(courseID):
            return HttpResponse("Not a valid course id", content_type="text/plain")

        courseObject = getCourseByID(courseID)
        if not courseObject.tutors.filter(pk=request.user.pk).exists():
            return HttpResponse('Course not supervised by you')

        if courseObject.class_list.filter(student_id=id).exists():
            return HttpResponse("Student already taking course: " + courseObject.name, content_type="text/plain")

        student = get_or_create_student(id, first_name, last_name)

        courseObject.class_list.add(student)
        courseObject.save()
        return HttpResponse(student.student_id + " is added to course " + courseObject.name, content_type="text/plain")

    else:
        return HttpResponse("Not a POST request", content_type="text/plain")


@login_required
def delete_student(request):
    if request.method == "POST":
        try:
            student_id = request.POST['student_id']
            course_id = request.POST['course_id']
        except KeyError:
            return HttpResponse("You must specify student_id and course id")

        if not course_exists(course_id):
            return HttpResponse("course id is not valid")

        course_object = getCourseByID(course_id)
        if not course_object.tutors.filter(pk=request.user.pk).exists():
            return HttpResponse('Course not supervised by you')

        try:
            if course_object.class_list.filter(student_id=student_id).exists():
                student = Student.objects.get(student_id=student_id)
                course_object.class_list.remove(student)
                course_object.save()
                return HttpResponse("student is deleted", content_type="text/plain")
            else:
                return HttpResponse("student " + student_id + " is not registered in " + courseObject.name,
                                    content_type="text/plain")

        except ValueError:
            return HttpResponse("Student ID is not valid for filtering", content_type="text/plain")
    else:
        return HttpResponse("Not a POST request", content_type="text/plain")


@login_required
def update_student(request):
    if request.method == "POST":
        try:
            student_id = request.POST['id']
            text = request.POST['text']
            field = request.POST['column_name']
        except KeyError:
            return HttpResponse("You must specify student_id, new text, and field to change")

        try:
            student = Student.objects.get(student_id=student_id)
            if field == "first_name":
                student.set_firstname(text)
            elif field == "last_name":
                student.set_lastname(text)
            student.save()
            return HttpResponse("updated the student's " + field, content_type="text/plain")

        except Student.DoesNotExist:
            return HttpResponse("Student is not found", content_type="text/plain")

    else:
        return HttpResponse("Not a POST request", content_type="text/plain")


'''
-----------------------------------------------------------------------------------------------------------------------------------
'''


def add_students_by_file(request):
    if request.method == "POST":
        try:
            staff = request.user
            students = json.loads(request.POST['students'])
            courses = request.POST.getlist('courses[]')
        except KeyError:
            return HttpResponse('you must specify students, and courses')

        # checking if the lists contains valid input
        # ----------------------------------------------
        valid_course = []

        if len(courses) == 0 or len(students) == 0:
            return HttpResponse('Please select courses or enter students')
        else:
            for c in courses:
                if course_exists(c) and staff.course_set.filter(pk=c).exists():
                    valid_course.append(c)

        if len(valid_course) == 0:
            return HttpResponse('no course is valid')

        # getting all the students objects
        student_obj_list = []
        for student in students:
            id = student.get("ID")
            firstname = student.get("Firstname")
            lastname = student.get("Surname")

            if id is None or firstname is None or lastname is None:
                return HttpResponse('CSV file\'s header is not valid')
            else:
                student_object = get_or_create_student(id, firstname, lastname)
                student_obj_list.append(student_object)

        # adding students to each course
        for course_id in valid_course:
            course_object = getCourseByID(course_id)
            course_object.class_list.add(*student_obj_list)
            course_object.save()
        return HttpResponse('Students are added to selected courses')
    else:
        return HttpResponse('Not a POST request')


def get_or_create_student(id, first_name, last_name):
    student, created = Student.objects.get_or_create(student_id=id)
    if created:
        student.set_firstname(first_name)
        student.set_lastname(last_name)
        student.save()

    return student


def course_exists(id):
    course_object = getCourseByID(id)
    if course_object is None:
        return False
    else:
        return True


'''
-----------------------------------------------------------
-------------------- assignment feedback ------------------
'''


@login_required
def assignment_feedback(request, assignment_title_slug):
    context = {}
    if request.method == "GET":

        staff = request.user
        # check staff is valid to see the assignment
        if not Assignment.objects.filter(slug=assignment_title_slug).exists():
            return HttpResponse('Not a valid assignment')

        assignment = Assignment.objects.get(slug=assignment_title_slug)
        if not assignment.course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('assignment not in your course list')

        students = assignment.course.class_list.all()

        context['students'] = students
        feedbacks = {}
        for student in students:
            if not FeedbackToStudent.objects.filter(student=student, assignment=assignment).exists():
                feedbacks[student] = False
            else:
                feedbacks[student] = True

        context['feedbacks'] = feedbacks

        return render(request, 'FeedbackSystem/assignmentFeedback.html', context)

    else:
        return HttpResponse('Not a GET request')


@login_required
def student_feedback(request, assignment_title_slug, student_id):
    context = {}

    if request.method == "GET":
        staff = request.user
        # checking valid assignment
        if not Assignment.objects.filter(slug=assignment_title_slug).exists():
            return HttpResponse('Not a valid assignment')

        assignment = Assignment.objects.get(slug=assignment_title_slug)
        if not assignment.course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('assignment not in your course list')

        if not Student.objects.filter(student_id=student_id).exists():
            return HttpResponse('Not a valid student id')

        if not assignment.course.class_list.filter(student_id=student_id).exists():
            return HttpResponse('Student not taking course: ' + assignment.title)

        student = assignment.course.class_list.get(student_id=student_id)

        # general feedback of assignment

        general_comments = Comment.objects.filter(isGeneral=True, assignment=assignment).order_by('-usedNum')

        student_specific = FeedbackToStudent.objects.filter(student=student, assignment=assignment)

        context['general_comments'] = general_comments

        context['specific_comments'] = student_specific

        # text = "assignment_slug : %s \n student_id : %s" % (assignment_title_slug, student_id)

        return render(request, 'FeedbackSystem/feedback.html', context)
    else:
        return HttpResponse('Not a GET request')


@login_required
def assignment_comments(request, assignment_title_slug):
    context = {}
    if request.method == "GET":
        try:
            staff = request.user
            # assignment_title_slug = request.POST['assignment_title_slug']
        except KeyError:
            return HttpResponse('you must specify assignment_title_slug')

        if not Assignment.objects.filter(slug=assignment_title_slug).exists():
            return HttpResponse('Not a valid assignment')

        assignment = Assignment.objects.get(slug=assignment_title_slug)
        if not assignment.course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('assignment not in your course list')

        general_comments = Comment.objects.filter(isGeneral=True, assignment=assignment).order_by('-usedNum')

        context['general_comments'] = general_comments

        return render(request, 'FeedbackSystem/generalComments.html', context)
    else:
        return HttpResponse('Not a POST request')


@login_required
def get_student_feedback(request, assignment_title_slug, student_id):
    if request.method == "GET":
        context = {}
        staff = request.user

        if not is_valid_assignment(staff, assignment_title_slug):
            print "not valid assignment"
            return HttpResponse('not a valid assignment slug')

        assignment = Assignment.objects.get(slug=assignment_title_slug)

        if not assignment.course.class_list.filter(student_id=student_id).exists():
            print "not valid student"
            return HttpResponse('Student not taking the course')

        student = assignment.course.class_list.get(student_id=student_id)
        feedback = FeedbackToStudent.objects.filter(student=student, assignment=assignment)

        context['feedback'] = feedback
        return render(request, 'FeedbackSystem/studentFeedback.html', context)

    else:
        return HttpResponse('Not a GET request')


# @login_required
# def student_feedback(request):
#     context = {}
#     if request.method == "POST":
#         try:
#             staff = request.user
#
#             student_id = request.POST['student_id']
#         except KeyError:
#             return HttpResponse('you must specify student_id')
#
#         if not Student.objects.filter(student_id=student_id).exists():
#             return HttpResponse('Not a valid student id')
#
#
#
#     else:
#         return HttpResponse('Not a POST request')

def get_comment(comment_id):
    if Comment.objects.filter(pk=comment_id).exists():
        return Comment.objects.get(pk=comment_id)
    else:
        return None


@login_required
def add_comment(request):
    if request.method == "POST":
        try:
            staff = request.user
            is_general = json.loads(request.POST['isGeneral'])
            student_id = request.POST['student_id']
            message = request.POST['message']
            assignment_title_slug = request.POST['assignment_title_slug']
        except KeyError:
            return HttpResponse('you must specify student id, text and assignment slug')

        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('not a valid assignment slug')

        assignment = Assignment.objects.get(slug=assignment_title_slug)

        print is_general
        if is_general:
            comnt = Comment.objects.create(message=message, isGeneral=True, assignment=assignment, usedNum=0)
            comnt.save()
            return HttpResponse('added a general comment')
        else:

            if assignment.course.class_list.filter(student_id=student_id).exists():
                student = assignment.course.class_list.get(student_id=student_id)

                comment = Comment.objects.create(message=message, assignment=assignment)
                comment.save()
                fts = FeedbackToStudent.objects.create(student=student, assignment=assignment, comments=comment)
                fts.save()
                return HttpResponse('added a specific comment')
            else:
                return HttpResponse('Student is not in your course list')
    else:
        return HttpResponse('Not a POST request')


@login_required
def add_general_comment_to_feedback(request):
    if request.method == "POST":
        try:
            staff = request.user
            comment_id = request.POST['comment_id']
            student_id = request.POST['student_id']
        except KeyError:
            return HttpResponse('you must specify comment id')

        comment = get_comment(comment_id)
        if (comment is None) or (not comment.isGeneral):
            return HttpResponse('not a valid general comment id')

        assignment_title_slug = comment.assignment.slug
        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('comment is not in your assignment list')

        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse('student id is not valid')

        comment.add_count()
        comment.save()
        fts = FeedbackToStudent.objects.create(student=student, assignment=comment.assignment, comments=comment)
        fts.save()
        return HttpResponse('comment added to feedback')

    else:
        return HttpResponse('Not a POST request')


@login_required
def update_comment(request):
    if request.method == "POST":
        try:
            staff = request.user
            comment_id = request.POST['pk']
            message = request.POST['value']
        except KeyError:
            return HttpResponse('you must specify comment id and text')

        comment = get_comment(comment_id)
        if comment is None:
            return HttpResponse('Not a valid comment')

        assignment_title_slug = comment.assignment.slug
        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('comment is not in your assignment list')

        comment.set_message(message)
        comment.save()
        return HttpResponse('Comment text updated')
    else:
        print 'not a POST request'
        return HttpResponse('Not a POST request')


def is_valid_assignment(user, assignment_title_slug):
    if not Assignment.objects.filter(slug=assignment_title_slug).exists():
        return False

    assignment = Assignment.objects.get(slug=assignment_title_slug)
    if assignment.course.tutors.filter(pk=user.pk).exists():
        return True

    return False


@login_required
def delete_general_comment(request):
    if request.method == "POST":
        try:
            staff = request.user
            comment_id = request.POST['comment_id']
        except KeyError:
            return HttpResponse('you must specify comment id and text')

        # check if valid comment
        comment = get_comment(comment_id)
        if (comment is None) or (not comment.isGeneral):
            return HttpResponse('not a valid comment')

        # check valid assignment - course is supervised by the staff
        if not comment.assignment.course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('assignment is not supervised by you')

        # delete comment
        comment.delete()
        return HttpResponse('comment is deleted')
    else:
        return HttpResponse('Not a POST request')


@login_required
def delete_from_feedback(request):
    if request.method == "POST":
        try:
            staff = request.user
            feedback_id = request.POST['feedback_id']
        except KeyError:
            return HttpResponse('you must specify feedback id')

        try:
            feedback = FeedbackToStudent.objects.get(pk=feedback_id)
        except FeedbackToStudent.DoesNotExist:
            return HttpResponse('Not a valid feedback comment')

        if not feedback.assignment.course.tutors.filter(pk=staff.pk).exists():
            return HttpResponse('assignment is not supervised by you')

        comment = feedback.comments

        if comment.isGeneral:
            if comment.usedNum > 0:
                comment.sub_count()
                comment.save()
            feedback.delete()

        else:
            comment.delete()

        return HttpResponse('feedback comment deleted')

    else:
        return HttpResponse('Not a POST request')


@login_required
def get_general_comments_used_valuse(request):
    data = {}
    if request.method == "POST":
        try:
            staff = request.user
            assignment_title_slug = request.POST['assignment_title_slug']
        except KeyError:
            return HttpResponse('You must specify assignment slug')

        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('comment is not in your assignment list')

        assignment = Assignment.objects.get(slug=assignment_title_slug)

        general_comments = Comment.objects.filter(isGeneral=True, assignment=assignment)

        for comment in general_comments:
            data[comment.pk] = comment.usedNum

        return JsonResponse(data)

    else:
        return HttpResponse('Not a POST request')


'''-----------------------------------------------------------------------------------------------
----------------------------------------- Download file or Zip -----------------------------------'''

from wsgiref.util import FileWrapper
from django.core.files.temp import NamedTemporaryFile


def student_file(request, assignment_title_slug, student_id):
    if request.method == "GET":
        try:
            staff = request.user
        except KeyError:
            return HttpResponse('you must specify assignment_title_slug')

        if not Student.objects.filter(student_id=student_id).exists():
            return HttpResponse('Not a valid student id')

        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('Not a valid assignment')

        assignment = Assignment.objects.get(slug=assignment_title_slug)

        if not assignment.course.class_list.filter(student_id=student_id).exists():
            return HttpResponse('Student not taking course: ' + assignment.title)

        student = assignment.course.class_list.get(student_id=student_id)

        tempFile = make_temp_file(student, assignment)
        if tempFile is None:
            return HttpResponse('No feedback has specified to the student: %s' % student.student_id)

        response = HttpResponse(tempFile, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % student_id
        tempFile.close()
        return response
    else:
        return HttpResponse('Not a GET request')


def make_temp_file(student, assignment):
    feedback = student.feedbacktostudent_set.filter(assignment=assignment).order_by('pk')
    if len(feedback) > 0:
        tempFile = NamedTemporaryFile()
        head = "Assignment: %s \n" \
               "========================\n" \
               "Student ID: %s \n" \
               "Name: %s \n" \
               "========================\n\n" \
               "Feedback: \n" % (assignment.title, student.student_id, student.get_fullname())
        tempFile.write(head)
        for each_feedback in feedback:
            comment = each_feedback.comments.message
            tempFile.write(comment + '\n')

        tempFile.seek(0)
        return tempFile
    return None


def send_zipfile(request, assignment_title_slug):
    if request.method == "GET":
        try:
            staff = request.user
        except KeyError:
            return HttpResponse('you must specify assignment_title_slug')

        if not is_valid_assignment(staff, assignment_title_slug):
            return HttpResponse('Not a valid assignment')

        assignment = Assignment.objects.get(slug=assignment_title_slug)
        student_file = []
        students = assignment.course.class_list.all()
        for student in students:
            tempFile = make_temp_file(student, assignment)
            if tempFile is not None:
                student_file.append((student.student_id, tempFile))

        if len(student_file) == 0:
            return HttpResponse('You have not added feedback to any student yet')

        zip_subdir = assignment_title_slug
        zip_filename = "%s.zip" % zip_subdir

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        i = 0
        while i < len(student_file):
            zip_path = os.path.join(zip_subdir, '%s.txt' % student_file[i][0])

            # Add file, at correct path
            zf.write(student_file[i][1].name, zip_path)

            student_file[i][1].close()
            i += 1
        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
        # tempZip = tempfile.TemporaryFile()
        # archive = zipfile.ZipFile(tempZip, 'w')
        # archive.write(tempFile.name, 'file.txt')
        # archive.close()
        # wrapper = FileWrapper(tempZip)
        # response = HttpResponse(wrapper, content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename=test.zip'
        # response['Content-Length'] = tempZip.tell()
        # tempZip.seek(0)
        # return response

    else:
        return HttpResponse('Not a GET request')
