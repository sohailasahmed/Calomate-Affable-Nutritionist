from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

        widgets = {
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'medical_conditions': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'