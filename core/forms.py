from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.models import Posts
from core.validators import tag_validation
from .utils import extract_tags


class UserRegistrationForm(UserCreationForm):
        username = forms.CharField(widget=forms.TextInput(attrs = { 'class': 'form-control form-control-lg','id':'uname'}),required=True)
        email = forms.EmailField(widget=forms.TextInput(attrs = { 'class': 'form-control form-control-lg'}),required=True)
        first_name = forms.CharField(widget=forms.TextInput(attrs = { 'class': 'form-control form-control-lg'}),required=True)
        last_name = forms.CharField(widget=forms.TextInput(attrs = { 'class': 'form-control form-control-lg'}),required=True)
        password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'class': 'form-control form-control-lg'}),required=True)
        password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class': 'form-control form-control-lg'}),required=True)
            
        class Meta:
            model = User
            fields = [ 'first_name','last_name','email','username','password1','password2']

        def clean_email(self):  #clean_<field name> is used for function name
            email = self.cleaned_data['email']
            if User.objects.filter(email = email).exists():
                raise forms.ValidationError("Email already exists")
            return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True)


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control fw-bold'
    }),required=True)
    body = forms.CharField(widget = CKEditorUploadingWidget(attrs={'class':'form-control'}),required=True)
    tags = forms.CharField(validators=[tag_validation],widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'maximum 3 tags  (eg:#devlog)'
    }),required=True)

    class Meta:
        model = Posts
        fields = ['title','body','tags','coverimage']



    