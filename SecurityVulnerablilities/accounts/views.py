from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import Student, Grade
from accounts.forms import RegisterForm, LoginForm, StudentsForm, SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 首頁
@login_required(login_url="Login")
def index(request): 
    return render(request, 'accounts/index.html')

# 登入
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')  # 如果使用者已經登入，直接導向首頁
    
    if request.method == "POST":
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            remember_me = request.POST.get("remember_me")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('/')  # 導向到首頁
        else:
            message = '驗證碼錯誤!'
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', locals())


# 登出
def log_out(request):
    logout(request)
    return redirect('/')
  
# 註冊
def register(request):
    # 如果使用者已經登入，直接導向首頁
    if request.user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print('PSOT')
        if form.is_valid():
            print('VALID')
            # 儲存 User 物件到資料庫並取得已創建的 User 物件
            user = form.save()

            # 創建 UserProfile 物件
            # profile = UserProfile()
            # profile.user = User.objects.get(id=user.id)
            # profile.user_name = user.username
            # profile.email = user.email

            # profile.save()  # 儲存 UserProfile 物件到資料庫

            return HttpResponse('<script>alert("註冊成功！"); window.location.href = "/login";</script>')
        else:
            print('INVALID')
            message = ''
            for error in form.errors:
                message += (error + "\n")

    return render(request, 'accounts/register.html', locals())

def xss_vulnerable(request):
    if request.method == 'POST':
        message = request.POST.get('message')
    return render(request, 'accounts/xss.html', locals())

def grade_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        results = Student.objects.raw('SELECT * FROM accounts_student WHERE name = %s', ['admin'])
        print(results)
    else:
        form = SearchForm()        
    return render(request, "accounts/grade_search.html", locals())

def student_maintenance(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
    else:
        form = StudentsForm()
    return render(request, "accounts/student_maintenance.html", locals())