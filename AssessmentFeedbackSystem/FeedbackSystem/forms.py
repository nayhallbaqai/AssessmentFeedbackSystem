from django import forms
from FeedbackSystem.models import *

class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title')