from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput

from django.core.mail import send_mail
from django.conf import settings
from .mail import send_mail_template

class FormLogin(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'validate','placeholder': 'Usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Senha'})
    )

class FormRegister(UserCreationForm):

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        help_text="Entre com um e-mail válido!",
    )

    first_name = forms.CharField(
        label="Primeiro Nome",
        widget=forms.TextInput(attrs={'autocomplete': 'first_name'}),
        help_text="Primeiro nome",
    )

    last_name = forms.CharField(
        label="Último Nome",
        widget=forms.TextInput(attrs={'autocomplete': 'last_name'}),
        help_text="Último nome",
    )

    #new
    def send_mail(self):
        email = self.cleaned_data["email"]
        subject = 'Ativar Cadastro'
        context = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],

        }
        template_name = 'registration/validate_send_email.html'
        send_mail_template(
            subject, template_name, context, [email]
        )

    #new
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Usuário'})
        self.fields['first_name'].widget.attrs.update({'placeholder':'Primeiro Nome'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Último Nome'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Senha'})        
        self.fields['password2'].widget.attrs.update({'placeholder':'Repetir Senha'})

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Já existe no cadastro um usuário com este nome.',
            },
        }

class FormPasswordReset(PasswordResetForm):

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'E-mail'})
    )

class FormPasswordConfirm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Nova Senha'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirme a Senha'}),
    )

class FormPasswordChange(PasswordChangeForm):

    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "Senha antiga foi digitada incorretamente.",
    }

    old_password = forms.CharField(
        label= "Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'placeholder': 'Senha Antiga'}),
    )

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Nova Senha'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirme a Senha'}),
    )

class FormEmailChange(forms.Form):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Senha'})
    )

    new_email = forms.EmailField(
        label="Novo E-mail",
        widget=forms.EmailInput(attrs={'autocomplete': 'email_change', 'placeholder': 'Novo E-mail'}),
        help_text="Entre com um e-mail válido!",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FormEmailChange, self).__init__(*args, **kwargs)

    def validate_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if not self.user.check_password(confirm_password):
            return False
        else:
            return True

    def validate_new_email(self):
        old_email = self.user.email
        new_email = self.cleaned_data.get('new_email')
        if new_email and old_email:
            if new_email == old_email:
                return False
            else:
                return True

    def save(self, commit=True):
        new_email = self.cleaned_data["new_email"]
        self.user.email = new_email
        if commit:
            self.user.save()
        return self.user