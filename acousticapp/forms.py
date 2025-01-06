from django import forms
from acousticapp.models import Answer, Comment

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('mos',)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        for field_name in self.Meta.fields:
            self.fields[field_name].required = True  # フィールドを必須にする


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)