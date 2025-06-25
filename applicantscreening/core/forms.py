# from django import forms
# from .models import JobListings, Application, InterviewSchedule, HiringDecision

# class JobListingsForm(forms.ModelForm):
#     class Meta:
#         model = JobListings
#         fields = '__all__'

# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['job', 'applicant', 'status']

# class InterviewScheduleForm(forms.ModelForm):
#     class Meta:
#         model = InterviewSchedule
#         fields = ['job', 'application', 'recruiter', 'date', 'time', 'status']

# class HiringDecisionForm(forms.ModelForm):
#     class Meta:
#         model = HiringDecision
#         fields = ['job', 'applicant', 'final_status', 'decision_date']

from django import forms
from .models import Applicant
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class ApplicantForm(forms.ModelForm):
    class Meta:
        model  = Applicant
        fields = ["contact_number", "experience", "skills", "education"]
        widgets = {
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        cpw = cleaned_data.get("confirm_password")

        if pw != cpw:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
