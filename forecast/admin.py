from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from .models import NewsPost


class NewsPostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = NewsPost
        fields = '__all__'

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostAdminForm