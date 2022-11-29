from django import forms
from home.models import Users
from home.models import Application
from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.models import User

class Userlogin(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())



class RegUser(forms.ModelForm):  
    username=forms.CharField(max_length=100)
    email=forms.EmailField(max_length=100)
    phone=forms.IntegerField()
    password=forms.CharField(max_length=100)
    confirm=forms.CharField(max_length=100)
    class Meta:
        model = Users
        fields = ['username','email','phone','password','confirm']
   
    
    def save(self, commit=True):
        user = super(RegUser, self).save(commit=False)
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user

class ApplicationForm(forms.Form):
    username = forms.CharField(max_length=100)
    CHOICES = [('M','MALE'),('F','FEMALE')]
    gender=forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
    email=forms.EmailField(max_length=100)
    income=forms.IntegerField()
    OCCUPATION_CHOICES =[
    (1,'Professional'),(0,'Daily Wages')]
    occupation=forms.IntegerField(label='Occupation', widget=forms.Select(choices=OCCUPATION_CHOICES))
    CATEGORY_CHOICES =[
    (0,'APL'),(1,'BPL') ]
    category=forms.IntegerField(label='Category', widget=forms.Select(choices=CATEGORY_CHOICES))
    place=forms.CharField(max_length=100)
    institute=forms.CharField(max_length=100)
    source=forms.CharField(max_length=100)
    destination=forms.CharField(max_length=100)
    class Meta:
        model = Application
        fields = ['username','gender','income','occupation','category','place','institute','source','destination']


    def clean(self):
        cleaned_data = super(ApplicationForm, self).clean()
        source = cleaned_data.get("source")
        destination = cleaned_data.get("destination")

        if source == destination:
            self._errors['source'] = self.error_class(['Both source and destination is same'])
            del self.cleaned_data['source']

        return cleaned_data
