from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        f_name = request.POST['firstname']
        l_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        country = request.POST['country']
        role = request.POST['role']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username Taken')
                print('User name taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already in use')
                print('Email exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=f_name, last_name=l_name,
                                                email=email, password=password)

                user.save()
                user_instance = User.objects.get(username=username)
                extra = Account(user=user_instance, country=country, role=role)
                extra.save()
                messages.success(request, 'Signup successful')
                print('user created')
            return redirect('login')
        else:
            messages.error(request, 'Password mismatch')
            print('Password not matching')
            return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'user_registration_form.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            print('Success')
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            print('Unsuceesful')
            return redirect('login')
    else:
        return render(request, 'window_Login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def forgotpass(request):
    return render(request, 'forgotpassword.html')
