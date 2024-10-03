"""
@Time ： 2024-10-03
@Auth ： Adam Lyu
"""
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required.")
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade < 1 or grade > 12:
            raise forms.ValidationError("Grade must be between 1 and 12.")
        return grade

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        enrollment_date = cleaned_data.get('enrollment_date')

        if date_of_birth and enrollment_date:
            if enrollment_date <= date_of_birth:
                raise forms.ValidationError(
                    "Enrollment date must be after date of birth."
                )
        return cleaned_data
