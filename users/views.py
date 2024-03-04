from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import CustomUser as User
from .models import Jobseeker, JobProvider
from django.urls import reverse
from PIL import Image
from PIL import UnidentifiedImageError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime
import PyPDF2

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            f_name = request.POST['firstname']
            l_name = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['confirm_password']
            country = request.POST['country']
            mob = request.POST['mob']
            dob = request.POST['dob']

            user_type = 'Job Seeker'
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, 'Username Taken')
                    print('User name taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email is already in use')
                    print('Email exists')
                    return redirect('register')
                elif User.objects.filter(mobile_number=mob).exists():
                    messages.warning(
                        request, 'Mobile number is already in use')
                    print('Mobile is in use')
                    return redirect(register)
                else:
                    user = User.objects.create_user(username=username, first_name=f_name, last_name=l_name,
                                                    email=email, password=password, country=country, mobile_number=mob, dob=dob, user_type=user_type)

                    user.save()
                    user_instance = User.objects.get(username=username)
                    seeker = Jobseeker.objects.create(username=user_instance)
                    seeker.save()
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
            if user.user_type == 'Job Provider':
                messages.success(request, 'Login Successful')
                print('Success')
                return redirect('providerhome')

            elif user.user_type == 'Job Seeker':
                messages.success(request, 'Login Successful')
                print('Success')
                return redirect('index')

            elif user.user_type == 'admin':
                return redirect('admin')

        else:
            messages.info(request, 'Invalid Credentials')
            print('Unsuccessful')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'window_Login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def forgotpass(request):
    return render(request, 'forgotpassword.html')


def provider_regi(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST['username']
        f_name = request.POST['firstname']
        l_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        country = request.POST['country']
        mob = request.POST['mob']
        dob = request.POST['dob']

        user_type = 'Job Provider'
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username Taken')
                print('Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already in use')
                print('Email exists')
                return redirect('register')
            elif User.objects.filter(mobile_number=mob).exists():
                messages.warning(request, 'Mobile number is already in use')
                print('Mobile is in use')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=f_name,
                    last_name=l_name,
                    email=email,
                    password=password,
                    country=country,
                    mobile_number=mob,
                    dob=dob,
                    user_type=user_type
                )

                provider = JobProvider.objects.create(user=user)
                provider.save()

                messages.success(request, 'Provider registration successful')
                print('User created')
                return redirect('login')
        else:
            messages.error(request, 'Password mismatch')
            print('Password not matching')
            return redirect('register')
    else:
        return render(request, 'provider_regi.html')


def seekerprofile(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Job Seeker':
            seeker = Jobseeker.objects.filter(username=request.user.id)
            print(seeker)

            params = {
                'seeker': seeker,

            }

    return render(request, 'profile.html', params)


def information(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            resume = request.FILES.get('resume')
            if resume:
                print("working")
                if resume:
                    print("working")
                    if verify_pdf(resume):
                        job_seeker = Jobseeker.objects.get(
                            username=request.user)
                        job_seeker.resume.delete()
                        job_seeker.resume = resume
                        job_seeker.save()

                        messages.success(
                            request, 'Resume uploaded successfully.')
                    else:
                        messages.warning(
                            request, 'Invalid file type. Only pdf are allowed.')
                        print('Unsucessful')
                        return redirect('seekerprofile')

            print(resume)
            updated_data = {
                'education': request.POST.get('education'),
                'skills': request.POST.get('skills'),
                'work_experience': request.POST.get('work_experience'),
            }
            try:
                Jobseeker.objects.filter(
                    username=request.user.id).update(**updated_data)
                messages.success(
                    request, 'Changes Successful.')
                print('sucessful')
            except Exception:
                messages.error(
                    request, 'Error in Uploading.')
                print('Unsucessful')
                return redirect('seekerprofile')
    return redirect('seekerprofile')


def verify_image(file):
    try:
        image = Image.open(file)
        image.verify()
        return True
    except UnidentifiedImageError:
        return False


def verify_pdf(file):
    try:
        pdf = PyPDF2.PdfReader(file)
        return True
    except FileNotFoundError:
        return False


def account(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            mob = request.POST['mob']

            country = request.POST['country']
            address = request.POST['address']
            profileimg = request.FILES.get('profileimg')
            if fname and lname and email and mob and country and address:
                try:
                    user = request.user
                    user.first_name = fname
                    user.last_name = lname
                    user.email = email
                    user.mobile_number = mob

                    user.country = country
                    user.save()
                    seeker = Jobseeker.objects.get(username=user)
                    seeker.address = address
                    seeker.save()
                    if profileimg:
                        print("working")
                        if verify_image(profileimg):
                            job_seeker = Jobseeker.objects.get(
                                username=request.user)
                            if job_seeker.profile_img.name != 'profiles/profile.png':
                                # Delete the existing profile image
                                job_seeker.profile_img.delete()
                            job_seeker.profile_img = profileimg
                            parent = job_seeker.username
                            parent.profile_img = profileimg
                            parent.save()
                            job_seeker.save()

                            messages.success(
                                request, 'Profile image uploaded successfully.')
                        else:
                            messages.warning(
                                request, 'Invalid file type. Only images are allowed.')
                            print('Unsucessful')
                            return redirect('seekerprofile')

                    print(profileimg)
                    messages.success(request, 'Update successful')
                except Exception as e:
                    messages.warning(request, f'Error in saving: {str(e)}')
            else:

                messages.warning(request, 'Please enter all feilds')
    return redirect('seekerprofile')


def profile(request):
    if request.user.user_type == "Job Seeker":
        return redirect('seekerprofile')
    elif request.user.user_type == "Job Provider":
        return redirect('providerhome')
    else:
        return redirect('/')


def passwordupdate(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            oldpassword = request.POST['oldpassword']
            newpassword = request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']
            user = request.user
            if user.check_password(oldpassword):
                if newpassword:
                    if confirmpassword == newpassword:
                        try:
                            # Validate the new password against Django's built-in password validators
                            validate_password(newpassword, user=user)
                        except ValidationError as validation_errors:
                            # Handle password validation errors
                            for error in validation_errors:
                                messages.error(request, error)
                        else:
                            # Set the new password for the user
                            user.set_password(newpassword)
                            # Save the updated user object
                            user.save()
                            # Update the user's session authentication hash
                            update_session_auth_hash(request, user)
                            messages.success(
                                request, 'Password Changed Successfully')
                    else:
                        messages.error(request, 'Password mismatch')
                        print('False')
                else:
                    messages.error(request, 'Password is cannot be blank')
                    print('False')
            else:
                messages.error(request, 'Old password is incorrect')

            return redirect('profile')


def providerupdate(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            mob = request.POST['mob']
            dob = request.POST['dob']
            country = request.POST['country']

            if fname and lname and email and mob and dob and country:
                try:
                    user = request.user
                    user.first_name = fname
                    user.last_name = lname
                    user.email = email
                    user.mobile_number = mob
                    dob_date = datetime.strptime(
                        dob, '%B %d, %Y').strftime('%Y-%m-%d')
                    user.dob = dob_date
                    user.country = country
                    user.save()
                    messages.success(request, 'Update successful')
                except Exception as e:
                    messages.warning(request, f'Error in saving: {str(e)}')

            else:
                messages.warning(request, 'Please enter all feilds')
    return redirect('providerhome')


def companyupdate(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            companyname = request.POST['companyname']
            companywebsite = request.POST['companywebsite']
            companydescription = request.POST['companydescription']
            companyimg = request.FILES.get('companyimg')

            if companyname and companywebsite and companydescription:
                try:
                    print("test")
                    provider = JobProvider.objects.get(
                        user=request.user.id)
                    company = provider.company  # Get the associated Company instance

                    # Update the Company instance fields
                    company.name = companyname
                    company.website = companywebsite
                    company.description = companydescription

                    # Save the Company instance to persist the changes
                    company.save()

                    if companyimg:
                        print("working")
                        if verify_image(companyimg):

                            company.image = companyimg
                            parent = provider.user
                            parent.profile_img = companyimg
                            parent.save()
                            company.save()
                            messages.success(
                                request, 'Profile image uploaded successfully.')
                        else:
                            messages.warning(
                                request, 'Invalid file type. Only images are allowed.')
                            print('Unsucessful')
                            return redirect('providerhome')
                    messages.success(request, 'Update successful')
                except Exception as e:
                    messages.warning(request, f'Error in saving: {str(e)}')

            else:
                messages.warning(request, 'Please enter all feilds')
    return redirect('providerhome')
