from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q
from datetime import datetime, date, timedelta
# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                new_profile = Students.objects.create(user=user_model, id=user_model.id)
                new_profile.save()
                return redirect('/home')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/signup')
    else:
        return render(request, 'core/register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/signin')
    else:
        return render(request, 'core/login.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin')

@login_required(login_url='/signin')
def home(request):
    courses = Courses.objects.all()
    student = Students.objects.filter(user = request.user).first()
    my_courses = studentsReg.objects.filter(studentId= student)
    response =[]
    now = datetime.now()
    for s in my_courses:
        c = Courses.objects.filter(code=s.courseId.code)[0]
        
        course_start_datetime = datetime.combine(date.today(),c.scheduleid.startTime)
        difference = course_start_datetime - now - timedelta(minutes=10)
        if difference.total_seconds() < 60:
            notifications = {'course_name': c.name,'start_time':c.scheduleid.startTime}
            response.append(notifications)
    if request.method == "POST":
        search = request.POST.get('search')
        courses = Courses.objects.filter(Q(name__icontains=search))
    return render(request,'core/home.html',{'notifications':response,'courses':courses})

@login_required(login_url='/signin')
def coures_details(request,pk):
    course = Courses.objects.filter(code = pk)[0]
    prerequisites = course.prerequisites.all()
    return render(request,'core/course.html',{'course':course,'prerequisites':prerequisites})

@login_required(login_url='/signin')
def course_select(request,pk):
    course = Courses.objects.filter(code=pk)[0]
    student = Students.objects.filter(user = request.user)[0]
    print(len(studentsReg.objects.filter(studentId=student,courseId=course)))
    if len(studentsReg.objects.filter(studentId=student,courseId=course)) != 0:
        messages.info(request, 'you are aredy registered .')
        return redirect(f'/course-details/{pk}')
    if course.capacity == len(studentsReg.objects.filter(courseId=course)):
        messages.info(request, 'this course is Full .')
        return redirect(f'/course-details/{pk}')
    schedule_this_course = course.scheduleid.startTime
    for c in studentsReg.objects.filter(studentId=student):
        if c.courseId.scheduleid.startTime == schedule_this_course:
            messages.info(request, f'Conflict with {c.courseId.name} lecture .')
            return redirect(f'/course-details/{pk}')
    studentsReg.objects.create(studentId=student,courseId=course)

    return redirect('/home')

@login_required(login_url='/signin')
def my_courses(request):
    studentsreg = studentsReg.objects.filter(studentId=Students.objects.filter(user=request.user)[0])
    courses=[]
    for s in studentsreg:
        courses.append(s.courseId)
    return render(request,'core/my-courses.html',{'courses':courses})

