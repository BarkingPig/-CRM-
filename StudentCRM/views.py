from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate,logout

# Create your views here.


def acc_login(request):
    """登陆"""
    errors = {}
    if request.method == "POST":
        _email = request.POST.get("email")
        _password = request.POST.get("password")

        user = authenticate(username = _email, password = _password)
        if user:
            login(request,user)
            next_url = request.GET.get("next","/")
            return redirect(next_url)
        else:
            errors['error'] = "用户名或密码错误!"


    return render(request,"login.html",{"errors":errors})



def acc_logout(request):
    """注销"""
    logout(request)
    return redirect("/account/login/")


def index(request):
    return render(request,'index.html')