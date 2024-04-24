from django.shortcuts import render,HttpResponseRedirect
from Project import models
from Project import graphs

# Create your views here.
def index(request):
    models.create_table()
    return render(request,'desktop-1.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data=models.retreive_data_user()
        # print(email,password)
        if email == data[0][0] and password == data[0][1]:
            return HttpResponseRedirect("home")
        else:
            return render(request,'login-page.html')
    else:
        return render(request,'login-page.html')
def signup(request):
    if request.method == "POST":
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        data=models.retreive_data_user()
        length = len(data)
        for i in range(length):
            if email == data[i][0]:
                return render(request,'sign-up-page.html')
        models.insert_data_user(fullname,email,password)
        # print(fullname,email,password)
        return HttpResponseRedirect('login')
    else:
        return render(request,'sign-up-page.html')
def dashboard(request):
    # models.create_table()
    # models.insert_data()
    # graphs.bar_char()
    return render(request,'dashboard.html')
def employee(request):
    data=[[1,2,3],[4,5,6]]
    return render(request,'employees.html',{'data':data})
def add_new_employee(request):
    return render(request,'add-a-new-employee.html')
def employee_added(request):
    return render(request,'employee-added.html')
def employee_details(request):
    return render(request,'view-employee-profile.html')
def meeting_shcheduler(request):
    return render(request,'meeting-scheduler.html')
def add_new_meeting(request):
    return render(request,'add-a-new-meeting.html')
def add_new_contact(request):
    return render(request,'add-a-new-contact.html')
def project(request):
    return render(request,'projects.html')
def add_new_project(request):
    return render(request,'add-a-new-project.html')
def project_added(request):
    return render(request,'project-added.html')
def project_details(request):
    return render(request,'projects-view-details.html')
def leads_pipeline(request):
    return render(request,'leads-pipeline.html')
