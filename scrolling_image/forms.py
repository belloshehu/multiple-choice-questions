from django import forms
from .models import ScrollingImage


class ScrollingImageForm(forms.ModelForm):

    class Meta:
        model = ScrollingImage
        fields = '__all__'
