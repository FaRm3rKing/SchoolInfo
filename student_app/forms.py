from django import forms

class EditProfileForm(forms.Form):
    # profile_picture = forms.ImageField(required=False)
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
                               label="Birthday",
                               required=False)
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id_for_label': 'email' } ),
    #                          max_length=64, 
    #                          label="Email",
    #                          required=False)
    phone = forms.CharField(
        label='Phone Number',
        max_length=11,
        required=False
    )
    address = forms.CharField(
        widget=forms.TextInput(),
        label='Address',
        required=False
    )
