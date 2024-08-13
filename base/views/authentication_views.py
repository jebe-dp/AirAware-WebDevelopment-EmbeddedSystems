from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . .models import User, Announcement
from . . forms import RegistrationForm

# Home
def home(request):
    last_announcement = Announcement.objects.last()
    context = {'last_announcement': last_announcement}
    return render(request, 'base/home.html', context)


# Authentication Functions
def register_page(request):
    if not request.user.is_authenticated:
        form = RegistrationForm()
        context = {'form': form}

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('user_dashboard')
            else: 
                # Add form errors to context
                context['form'] = form
                # Display form errors as messages
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")

        return render(request, 'base/register.html', context)
    else:
        return redirect('home')

def login_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            
            # Check if Username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
                return redirect('login')
            
            # Authenticate 
            user = authenticate(request, username=username, password=password)
            
            # If user was returned, login. Otherwise, invalid password
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('staff_dashboard')
                else:
                    return redirect('user_dashboard')
            else: 
                messages.error(request, "Invalid Password")
                return redirect('login')
            
        return render(request, 'base/login.html', context)
    else:
        # redirect to home if already authenticated
        return redirect('home')

def logout_client(request):
    logout(request)
    return redirect('home')
