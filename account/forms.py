from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from django.urls import reverse_lazy

from account.models import EmailAccount


class RegistrationForm(UserCreationForm):
    """
      Form for Registering new users
    """
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = EmailAccount
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields
        """
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (
                self.fields['email'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control '})


class AccountAuthenticationForm(forms.ModelForm):
    """
      Form for Logging in  users
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = EmailAccount
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields
        """
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class AccountUpdateForm(forms.ModelForm):
    """
      Updating User Info
    """

    class Meta:
        model = EmailAccount
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields
        """
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],):
            field.widget.attrs.update({'class': 'form-control '})

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = EmailAccount.objects.exclude(pk=self.instance.pk).get(email=email)
            except EmailAccount.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' already in use." % email)


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = EmailAccount
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = (
                                                "Raw passwords are not stored, so there is no way to see "
                                                "this user's password, but you can <a href=\"%s\"> "
                                                "<strong>Change the Password</strong> using this form</a>."
                                            ) % reverse_lazy('admin:auth_user_password_change', args=[self.instance.id])

    class Meta:
        model = EmailAccount
        fields = ('email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
