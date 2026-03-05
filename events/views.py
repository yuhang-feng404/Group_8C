from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Q
from .models import User  # 引入我们刚才自定义的 User 模型


def login_view(request):

    selected_role = request.GET.get('role', 'student')

    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')


        user = User.objects.filter(Q(email=account) | Q(phone_number=account)).first()


        if user and user.check_password(password):

            login(request, user)


            if user.role == User.STUDENT:
                return redirect('home')
            elif user.role == User.SOCIETY_ADMIN:
                return redirect('admin_dashboard')
        else:

            context = {
                'error': '账号或密码错误',
                'current_role': selected_role
            }
            return render(request, 'events/login.html', context)


    return render(request, 'events/login.html', {'current_role': selected_role})


def register_view(request):
    selected_role = request.GET.get('role', 'student')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {'current_role': selected_role}


        if len(password) < 8:
            context['error'] = '密码最少8位'
            return render(request, 'events/register.html', context)


        if password != confirm_password:
            context['error'] = '两次密码输入不一致'
            return render(request, 'events/register.html', context)


        if User.objects.filter(email=email).exists():
            context['error'] = '该邮箱已被注册'
            return render(request, 'events/register.html', context)


        db_role = User.STUDENT if selected_role == 'student' else User.SOCIETY_ADMIN


        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=db_role
        )

        user.first_name = name
        user.save()


        login(request, user)


        if db_role == User.STUDENT:
            return redirect('home')
        else:
            return redirect('admin_dashboard')


    return render(request, 'events/register.html', {'current_role': selected_role})

def landing_page(request):

    return render(request, 'events/landing.html')
