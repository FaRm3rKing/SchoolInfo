from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser

class CreateUserForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    GENDER_CHOICES = (("male", "Male"), 
                      ("female", "Female")
                      )

    fname=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              label="First Name"
                              )
    lname=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              label="Last Name"
                              )
    gender=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                         choices=GENDER_CHOICES,
                         label="Gender",
                         required=True
                         )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id_for_label': 'email' } ),
                             max_length=64, 
                             label="Email",
                             required="True")
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              label="Password"
                              )
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              label="Confirm Password"
                              )
    role=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                         choices=CustomUser.ROLE_CHOICES,
                         label="Role",
                         required=True
                         )
    class Meta:
        model = CustomUser
        fields = ['fname','lname', 'gender', 'email', 'password1', 'password2', 'role']


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ["email", "password", "role", "is_active", "is_admin"]


