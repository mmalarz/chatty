from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib import messages


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('accounts:login')
    else:
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)


def startpage(request):
    return render(request, 'accounts/startpage.html', {})


def settings(request, current_user):
    user = get_object_or_404(User, username=current_user)

    if user == request.user:

        if 'email' in request.POST:
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile details updated.')
            else:
                messages.error(request, 'Error: Profile details not updated.')
            return redirect('accounts:settings', current_user=request.user)

        elif 'new_password1' in request.POST:
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password has been changed.')
            else:
                messages.error(request, 'Error: Password has not been changed')
            return redirect('accounts:settings', current_user=request.user)

        else:
            user_form = EditProfileForm(instance=user)
            password_form = PasswordChangeForm(user=user)
            context = {
                'user_form': user_form,
                'password_form': password_form,
            }
            return render(request, 'accounts/settings.html', context)
    else:
        raise Http404
