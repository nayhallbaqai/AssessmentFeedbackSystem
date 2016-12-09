from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('course/')

    return HttpResponseRedirect('/accounts/login/')

@login_required
def course(request):
    context = {}
    context['user'] = request.user
    return render(request, 'FeedbackSystem/course.html', context)