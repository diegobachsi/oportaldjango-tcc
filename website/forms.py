from django import forms
from django.core.mail import send_mail
from django.conf import settings

from .mail import send_mail_template

class Contact(forms.Form):

    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nome'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    message = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'placeholder': 'Mensagem'}))

    def send_mail(self):
        subject = 'Contato/Dúvida'
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
            
        }
        template_name = 'contact_email.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )