from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminCreationForm,LoginForm
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')  
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            # Create admin
            try:
                User = get_user_model()
                if User.objects.filter(email=email).exists():
                    messages.warning(request,'A User with this email already exists')
                    return redirect('create_admin')
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username = username,
                    role='admin',
                    is_active=True,
                    is_staff=True, 
                    is_superuser = True,
                )
                user.set_password(password)  
                user.save()
                messages.success(request, 'Admin created successfully.')
                return redirect('admin_list')  # Redirect to a success page
            except Exception as e:
                form.add_error(None, str(e))  # Add general error to form
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('create_admin')
        else:
            for field in form.fields:
                css_class = 'form-control'
                if form[field].errors:
                    css_class += ' is-invalid'
                form.fields[field].widget.attrs.update({'class': css_class})
            return render(request, 'dashboard/addAdmin.html', {'form': form})

    else:
        form = AdminCreationForm()

    return render(request, 'dashboard/addAdmin.html', {'form': form})

@login_required(login_url='login')  
def admin_list(request):
    User = get_user_model()
    admins = User.objects.filter(is_superuser=True)
    return render(request,'dashboard/admin_list.html',{'admins':admins})

@login_required(login_url='login')  
def delete_admin(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    user.delete()
    messages.success(request, "admin deleted successfully")
    return redirect('admin_list')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect("dashboard")
            else:
                messages.error(request, "Username or password is not correct")
                return redirect('login')
        else:
            # If the form is invalid, show form errors
            messages.error(request, "Invalid login details")
    else:
        # Initialize the form for GET requests
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
