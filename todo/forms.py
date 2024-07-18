from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_at', 'completed', 'priority']

    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, label="Priority")