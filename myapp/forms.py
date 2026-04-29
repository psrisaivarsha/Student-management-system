from django import forms
from myapp.models import Student

class StudentForm(forms.ModelForm):

    def clean_stuMarks(self):
        marks = self.cleaned_data.get('stuMarks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise forms.ValidationError("Marks must be between 0 and 100")
        return marks

    def clean_stuName(self):
        name = self.cleaned_data.get('stuName')
        if name and not name.isalpha():
            raise forms.ValidationError("Name should contain only letters")
        return name

    class Meta:
        model = Student
        fields = ['stuId', 'stuName', 'stuMarks', 'stuEmail', 'photo']
        widgets = {
            'stuId': forms.NumberInput(attrs={'class': 'form-control'}),
            'stuName': forms.TextInput(attrs={'class': 'form-control'}),
            'stuMarks': forms.NumberInput(attrs={'class': 'form-control'}),
            'stuEmail': forms.EmailInput(attrs={'class': 'form-control'}),
        }