# dashboard/forms.py
from django import forms
from members.models import Member

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'course', 'year_of_study', 'profile_picture']

# Remove the AICourseGenerationForm since AIGeneratedCourse model no longer exists