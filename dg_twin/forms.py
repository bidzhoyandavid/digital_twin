from django import forms
from .models import Avatar

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['original_photo']
        widgets = {
            'original_photo': forms.FileInput(attrs={'accept': 'image/*'})
        } 