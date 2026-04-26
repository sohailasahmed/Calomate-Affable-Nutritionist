from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_pic',
            'city',
            'feet',
            'inches',
            'weight_kg',
            'dob',
            'gender',
            'goal',
            'target_weight',
            'medical_conditions'
        ]

        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in ['profile_pic', 'dob', 'medical_conditions']:
                field.widget.attrs.update({'class': 'form-control'})