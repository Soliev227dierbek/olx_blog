from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Review
class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Никнейм", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20'}))
    password1 = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control footer-input margin-b-20'}))
    password2 = forms.CharField(label="Повторите пароль", required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control footer-input margin-b-20'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20'}))
    first_name = forms.CharField(label="Имя", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20'}))
    last_name = forms.CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20'}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2", )
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            return user
        
class ProfileForm(forms.ModelForm):
    name = forms.CharField(label="Имя", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-20'}))
    avatar = forms.ImageField(label="Аватар", required=True,widget=forms.ClearableFileInput(attrs={'class' : 'form-control footer-input margin-b-20 m-20'}))
    bio = forms.CharField(label="Биография", required=True, widget=forms.Textarea(attrs={'class' : 'form-control footer-input margin-b-20, margin-left: 20px;'}))
    location = forms.CharField(label="Локация", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20', 'margin': 20}))

    class Meta:
        model = Profile
        fields = ("name", "avatar", "bio", "location")

    def delete_profile(self):
        if self.instance:
            user = self.instance.user
            self.instance.delete()
            user.delete()

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control my-2', 'rows': 4}),
        }