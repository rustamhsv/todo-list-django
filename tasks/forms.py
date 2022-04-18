from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
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

    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date']
        widgets = {
            'due_date': DateInput(),
        }
