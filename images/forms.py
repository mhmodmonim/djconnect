from django import forms
from .models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']

        widgets = {
            'url' : forms.HiddenInput
        }




    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        ext = url.rsplit('.', 1)[1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError('URL doesn\'t match valid image extensions')
        return url

    def save(self, force_insert=False,force_update=False,  commit=True):
            image = super().save(commit=False)
            image_url = self.cleaned_data['url']
            name = slugify(image.title)
            ext = image_url.rsplit('.',1)[1].lower()
            image_name = f"{name}.{ext}"
            #download image using requests lib
            res = requests.get(image_url)
            image.image.save(image_name,ContentFile(res.content), save=False)
            if commit:
                image.save()

            return image

