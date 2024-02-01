from django import forms

from .models import Option, Question


class QuestionForm(forms.ModelForm):
    # question = forms.Textarea()
    # option = forms.NullBooleanField()

    class Meta:
        model = Question
        fields = "__all__"
