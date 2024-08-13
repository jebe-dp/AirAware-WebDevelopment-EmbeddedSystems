from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from  . .models import PasswordChangeRequest, User
from functools import wraps

def staff_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')  
        elif not request.user.is_staff:
            return redirect('home')  
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


CustomUser = get_user_model()

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        middle_name = request.POST.get('middle_name')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = CustomUser.objects.get(username__iexact=username)
            if user.middle_name.lower() == middle_name.lower():
                if new_password == confirm_password:
                    hashed_password = make_password(new_password)
                    password_change_request = PasswordChangeRequest.objects.create(user_id=user.id, new_password=new_password)
                    return redirect('login')
                else:
                    return HttpResponse('Password and Password Confirmation did not match. Please try again.', status=400)
            else:
                return HttpResponse('Username and Middle Name did not match.', status=400)
        except CustomUser.DoesNotExist:
            return HttpResponse('Username does not exist.', status=400)
    return render(request, 'base/patient-section/reset_password.html')

@staff_login_required
def password_requests(request):
    password_change_requests = PasswordChangeRequest.objects.all()
    return render(request, 'base/staff-section/password_requests.html', {'password_change_requests': password_change_requests})

@staff_login_required
def approve_password_change(request, request_id):
    password_change_request = get_object_or_404(PasswordChangeRequest, pk=request_id)
    if request.method == 'POST' and request.POST.get('action') == 'approve':
        user = password_change_request.user
        user.set_password(password_change_request.new_password)
        user.save()
        password_change_request.delete()
        return HttpResponse('Change Password Request - Accepted')
    return HttpResponse(status=400)

@staff_login_required
def reject_password_change(request, request_id):
    password_change_request = get_object_or_404(PasswordChangeRequest, pk=request_id)
    if request.method == 'POST' and request.POST.get('action') == 'reject':
        password_change_request.delete()
        return HttpResponse('Change Password Request - Rejected')
    return HttpResponse(status=400)
