import uuid
from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from termcolor import colored

from Users.forms import SignUpForm
from Users.models import User
from utility.EmailService import EmailService


def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            valueNext = request.POST.get('next')

            return redirect(valueNext)
        else:
            # else => user is None
            messages.error(request, 'User not found')
            return redirect('login')


def MakeConfirmEmailCode(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def Confirm_email(request, UserCode):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Working on verification of user
        SentCode = request.POST['Email_Code']
        UserCode = request.POST['UserCode']
        user_model = get_user_model()
        user = user_model.objects.filter(confirmEmailCode=SentCode).first()
        if user:
            user.is_active = True
            user.isConfirmEmail = True
            user.uniqueCode = uuid.uuid4().hex[:16].upper()
            user.confirmEmailCode = MakeConfirmEmailCode(6)
            user.save(update_fields=['is_active', 'isConfirmEmail', 'uniqueCode', 'confirmEmailCode'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your registration was successful')
            return redirect('home')
        else:
            # else => SentCode is not correct
            user = User.objects.filter(uniqueCode__exact=UserCode).first()
            if user:
                tryTime = user.userTry
                if tryTime < 3:
                    user.userTry += 1
                    user.save()
                    return redirect('ConfirmEmail', f"{UserCode}")
                else:
                    user.delete()
                    messages.error(request, "You can't submit code again\nPlease fill form again")
                    return redirect('register')

    elif request.method == "GET":
        # Users is going to EnterCode page
        user_model = get_user_model()
        user = user_model.objects.filter(uniqueCode=UserCode).first()
        if not user:
            # UserCode is not correct
            raise Http404()
        # user IsExistsUser =so> User have to send code
        else:
            return render(request, 'email/EnterCode.html', context={'UserCode': UserCode,
                                                                    'userTry': 3 - user.userTry})

    else:
        # Something is wrong
        print(colored("Please check the << Confirm_email >> function in Users.views", 'red'))
        messages.error(request, "Something is wrong\nPlease try again")
        return redirect('home')


def Register_Login(request):
    if not request.user.is_authenticated:
        # User clicked on register/login button
        form = SignUpForm
        context = {'SUForm': form}  # SUForm = Sign Up Form
        return render(request, 'registration/login.html', context=context)
    else:
        # else => user is authenticated before
        return redirect('home')


@csrf_exempt
def SignUp(request):
    if request.method == "POST":
        if not request.is_ajax():
            form = SignUpForm(request.POST)
            if form.is_valid():
                User_data = form.save(commit=False)
                User_data.is_active = False
                User_data.confirmEmailCode = MakeConfirmEmailCode(6)
                User_data.isConfirmEmail = False
                User_data.uniqueCode = uuid.uuid4().hex[:16].upper()
                User_data.save()
                # Start: send_email
                context_email = {
                    'title': 'Confirmation email',
                    'description': f'Hi, {User_data.username}\nYour activation code is:',
                    'ConfirmEmail': User_data.confirmEmailCode
                }
                EmailService.send_email(
                    title='Verification email',
                    to=[User_data.email],
                    template_name='email/ConfirmEmail.html',
                    context=context_email
                )
                # End : send_email
                return redirect('ConfirmEmail', f"{User_data.uniqueCode}")

            else:
                # else => form is not valid
                messages.error(request, 'Form is not valid')
                return render(request, 'registration/login.html', {'SUForm': form})
        else:
            # else => request is AJAX
            emailAJ = request.POST.get('email')
            isExists = User.objects.filter(email__iexact=emailAJ).exists()
            return JsonResponse(data={'email': f"{not isExists}"})


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        # else => User is not authenticated =so> can't logging out
        messages.error(request, "You can't logging out right now")
        return redirect('home')
