from django.shortcuts import render,redirect,HttpResponse
from lmsapp.EmailBackend import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lmsapp.models import CustomUser,Course,Student,Session_Year,Staff
def BASE(request):
    return render(request,'base.html')
def LOGIN(request):
    return render(request,'login.html')
def LOGIN(request):
    return render(request,'login.html')
def doLogin(request):
    if request.method == "POST":
       user = EmailBackEnd.authenticate(request,
                                        username=request.POST.get('email'),
                                        password=request.POST.get('password'),)
       if user!=None:
           login(request,user)
           user_type = user.user_type
           if user_type == '1':
               return redirect('hod_home')
           elif user_type == '2':
               return redirect('staff_home')
           elif user_type == '3':
               return redirect('student_home')
           else:
               messages.error(request,'Email and Password Are Invalid !')
               return redirect('login')
       else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')
       
def doLogout(request):
    logout(request)
    return redirect('login')
@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)


    context = {
        "user":user,
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password !=None and password != "":
                customuser.set_password(password)
            if profile_pic !=None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,'Your Profile Updated Successfully !')
            return redirect('profile')
        except:
            messages.error(request,'Failed To Update Your Profile')

    return render(request,'profile.html')

def REGISTER_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        if not username or not password or not email:
            messages.warning(request, 'Username, Password, and Email are required fields.')
            return redirect('register_student')
        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('register_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('register_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )

            student.save()
            messages.success(request, 'Registered Successfully')
            return redirect('login')
    context = {
            'course':course,
            'session_year':session_year,
            }
    return render(request,'register_student.html',context)

def REGISTER_STAFF(request):
    if request.method == 'POST':
        profile_pic =request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email is already taken')
            return redirect('register_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Email is already taken')
            return redirect('register_staff')
        if not username or not password or not email:
            messages.warning(request, 'Username, Password, and Email are required fields.')
            return redirect('register_staff')
        else:
            user=CustomUser(first_name=first_name,last_name=last_name,email=email,username=username,profile_pic=profile_pic,user_type=2)
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request,'Registered Successfully')
            return redirect('login')

    return render(request,'register_staff.html')

def REGISTER(request):
    return render(request,'register.html')