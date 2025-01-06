from django import forms
from testapp.models import Acoustic, MosTest

class MosTestForm(forms.ModelForm):
    class Meta:
        model = MosTest
        fields = ['test_name', 'description', 'instruction']

