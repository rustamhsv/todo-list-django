from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tasks.models import Task


class DateInput(forms.DateInput):
    input_type = 'date'


class AddNewTaskForm(forms.ModelForm):
    # new_task = forms.CharField(max_length=100)
    # new_task_description = forms.CharField(max_length=200)
    def __init__(self, *args, **kwargs):
        super(AddNewTaskForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].help_text = ""
        self.fields['task_description'].help_text = ""
        self.fields['due_date'].help_text = ""
        # self.fields['user'].help_text = ""

    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'user', 'files', 'project']
        widgets = {
            'due_date': DateInput(),
        }


class AddMyTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMyTaskForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].help_text = ""
        self.fields['task_description'].help_text = ""
        self.fields['due_date'].help_text = ""
        # self.fields['user'] = 'rustam'

    class Meta:
        model = Task
        exclude = ['user']
        widgets = {
            'due_date': DateInput(),
        }


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #
    #     return user
