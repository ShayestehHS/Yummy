from django import forms

from Users.models import User
from Yummy.models import Restaurant, RestaurantImage


class AdminSectionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    phone_number = forms.IntegerField()
    logo = forms.FileField()

    class Meta:
        model = Restaurant
        fields = ('description', 'email', 'phone_number', 'logo')


class AdminSectionImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = RestaurantImage
        fields = ('image',)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'UserName'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'PassWord'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'ConPassWord'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password','confirm_password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            match = User.objects.get(username=username)
            raise forms.ValidationError('This username is already in use.')
        except User.DoesNotExist:
            return username  # Unable to find a user, this is fine

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
            raise forms.ValidationError('This email address is already in use.')
        except User.DoesNotExist:
            return email  # Unable to find a user, this is fine

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        else:
            return password
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        else:
            return user
