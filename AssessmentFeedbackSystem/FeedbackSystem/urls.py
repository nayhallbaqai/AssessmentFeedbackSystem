from django.conf.urls import url
from FeedbackSystem import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/$', views.course, name='course'),
    url(r'^getUserCourses/$', views.get_user_courses, name='getCourses'),
    url(r'^addCourse/$', views.add_course, name='add_course'),
    url(r'^deleteCourse/$', views.delete_course, name='deleteCourse'),
    url(r'^assignCourseToTutor/$', views.course_assignment_to_tutor, name='addCourseToTutor'),

    url(r'^ajax_assignment/$', views.get_assignments, name='ajax_assignment'),
    url(r'^addAssignment/$', views.add_assignment, name='addAssignment'),
    # student table urls
    url(r'^students/$', views.get_all_student, name='allStudents'),
    url(r'classList/$', views.get_course_class_list, name='course_class_list'),
    url(r'^addStudent/$', views.add_students, name='addStudent'),
    url(r'^changeStudent/$', views.update_student, name='editStudent'),
    url(r'^removeStudent/$', views.delete_student, name='deleteStudent'),
    # add student by csv url
    url(r'^addStudentByCSV/$', views.add_students_by_file, name='csv_add_student'),
    url(r'^update_general_comment/$', views.update_comment, name='edit_comment'),
    url(r'^add_comment/$', views.add_comment, name='addComment'),
    url(r'^delete_general_comment/$', views.delete_general_comment, name='deleteGeneralComment'),
    # url(r'^delete_from_feedback/$', views., name='deleteCommentFromFeedback'),
    url(r'^add_general_comment_to_feedback/$', views.add_general_comment_to_feedback, name='addGeneralCommentToStudentFeedback'),
    url(r'^delete_from_feedback', views.delete_from_feedback, name='deleteFeedbackComment'),
    url(r'^get_general_comment_usedNum', views.get_general_comments_used_valuse, name='getGeneralCommentUsedNum'),

    # each student feedback
    # url(r'^fetch_student_feedback/$', views.get_student_feedback, name='get_student_feedback'),

    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/$', views.assignment_feedback, name='assignment_feedback'),
    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/test_file/$', views.send_zipfile, name='feedback_zipfile'),
    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/fetch_general_comments/$', views.assignment_comments,
        name='get_general_comment'),
    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/(?P<student_id>[\w\-]+)/$', views.student_feedback,
        name='student_feedback'),
    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/(?P<student_id>[\w\-]+)/fetch_student_feedback/$', views.get_student_feedback, name='get_student_feedback'),
    url(r'^course/(?P<assignment_title_slug>[\w\-]+)/(?P<student_id>[\w\-]+)/test_file/$', views.student_file,
        name='feedback_file'),
]
