from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.contrib import messages 

from django.contrib.auth.models import User

from .forms import FormLogin, FormRegister, FormPasswordReset, FormPasswordConfirm, FormPasswordChange, FormEmailChange

class PasswordChange(PasswordChangeView):
    form_class = FormPasswordChange
    template_name = 'password/password_change.html'

class PasswordConfirm(PasswordResetConfirmView):
    form_class = FormPasswordConfirm
    template_name = 'password/password_reset_confirm.html'

class PasswordReset(PasswordResetView):
    form_class = FormPasswordReset
    template_name = 'password/password_reset_form.html'
    subject_template_name = 'password/password_reset_subject.txt'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        emails = [str(elem) for elem in list(User.objects.all().values_list('email'))]
        email = "('" + request.POST["email"] + "',)"
        if form.is_valid():
            if email in emails:
                return super().form_valid(form)
            else:
                messages.error(request, "Esse e-mail não está cadastrado.")

        return render(request, self.template_name, {'form': form})

class Login(LoginView):
    form_class = FormLogin

def logar(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('website:index')
        else:
            form = FormLogin()
    else:
        form = FormLogin()

    context['form'] = form

    return render(request, 'registration/login.html', context)

def cadastrar(request):
    context = {}
    if request.method == "POST":
        form = FormRegister(request.POST)
        if form.is_valid():
            form.save()
            form.send_mail() 
            context['is_valid'] = True
            context['form'] = form
            return render(request, 'registration/validate.html', context)
    else:
        form = FormRegister()

    context['form'] = form

    return render(request, 'registration/register.html', context)

def registerValidate(request, username): 

    user = User.objects.get(username=username)
    user.is_active = True
    user.save()

    return render(request, 'registration/validate_confirm.html')

@login_required(login_url='accounts:login')
def emailChange(request):
    context = {}
    if request.method == 'POST':
        form = FormEmailChange(request.user, request.POST)
        if form.is_valid():
            if form.validate_new_email():
                if form.validate_password():
                    form.save()
                    return render(request, 'registration/email_change_confirm.html')
                else:
                    messages.error(request, "Senha incorreta! Informe-a novamente.")
            else:
                messages.error(request, "Esse já é o e-mail atual.")
        
    else:
        form = FormEmailChange(request.user)

    context['form'] = form

    return render(request, 'registration/email_change.html', context)







