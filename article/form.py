from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from article.models import ContactUs, Comment


class Contact(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            "Name": forms.TextInput(attrs={
                'class': 'form-group col-xs-12 floating-label-form-group controls',
                'placeholder': 'نام'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'form-group col-xs-12 floating-label-form-group controls',
                'placeholder': 'ایمیل'
            }),
            "phone": forms.TextInput(attrs={
                'class': 'form-group col-xs-12 floating-label-form-group controls',
                'placeholder': 'شماره موبایل'
            }),
            "body": forms.Textarea(attrs={
                'class': 'form-group col-xs-12 floating-label-form-group controls',
                'placeholder': 'توضیحات'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 11:
            raise ValidationError('شماره موبایل باید 11 عدد باشد.')
        return phone

    def clean_Name(self):
        Name = self.cleaned_data.get('Name')
        if not Name.isalpha():
            raise ValidationError('نام معتبر نیست.')
        return Name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('ایمیل معتبر نیست.')
        return email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            "author": forms.TextInput(attrs={
                'class': 'form-group col-xs-6 floating-label-form-group controls',
                'placeholder': 'نام'
            }),
            "text": forms.Textarea(attrs={
                'class': 'form-group col-xs-6 floating-label-form-group controls',
                'placeholder': 'نظر'
            }),
        }