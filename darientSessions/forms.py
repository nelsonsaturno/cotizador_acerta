from django import forms
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}),
                                label="Repeat Password")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "username")

        widgets = {
            'password': forms.PasswordInput(),
        }

        labels = {
            'email': 'E-mail',
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Both passwords must be the same.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).count() != 0:
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count() != 0:
            raise forms.ValidationError(u'Username must be unique.')
        return username

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = 0
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        else:
            return user


class CorredorCreateForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}),
                                label="Repeat Password")
    licencia = forms.CharField(required=True,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nro. de Licencia'}))
    ruc = forms.CharField(required=True,
                          label="",
                          widget=forms.TextInput(attrs={'placeholder': 'RUC'}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "username")

        widgets = {
            'password': forms.PasswordInput(),
        }

        labels = {
            'email': 'E-mail',
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Both passwords must be the same.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).count() != 0:
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count() != 0:
            raise forms.ValidationError(u'Username must be unique.')
        return username

    def save(self, commit=True):
        user = super(CorredorCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = 0
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        else:
            return user


class LoginForm(forms.Form):

    username = forms.CharField(max_length=60, required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Clave'}), required=True, label='')
