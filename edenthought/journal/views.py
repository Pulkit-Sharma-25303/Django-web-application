from django.shortcuts import render,redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages


def homepage(request):
    return render(request,"index.html")





def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Created!")
            return redirect("my_login")
    context = {"RegistrationForm":form}
    return render(request,"register.html",context)
def my_login(request):

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username= request.POST.get("username")
            password= request.POST.get("password")

            user = authenticate(request, username=username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context={"LoginForm": form}
    return render(request,"my_login.html", context)





@login_required(login_url="my_login")
def dashboard(request):
    return render(request,"dashboard.html")
# Create your views here.


def user_logout(request):
    auth.logout(request)
    return redirect('homepage')

@login_required(login_url="my_login")
def create_thought(request):
    form = ThoughtForm()
    if request.method == "POST":
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            return redirect("dashboard")
    context={"CreateThoughtForm":form}
    return render(request,"create-thought.html",context)