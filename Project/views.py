from django.shortcuts import render,HttpResponseRedirect
from Project import models
from Project import graphs
# Create your views here.
user_id=0
def modify(id):
    global user_id
    user_id=id
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
            modify(data[0][2])
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
    

def add_new_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        phone = request.POST.get('contact')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        salary = int((request.POST.get('salary')),10)
        coun = request.POST.get('country')
        data=models.retreive_data_employee()
        length = len(data)
        for i in range(length):
            if email == data[i][0]:
                return render(request,'add-a-new-employee.html')
        models.insert_data_employee(name,designation,phone,email,gender,coun,salary,user_id)
        return HttpResponseRedirect('employee-added')
    else:
        return render(request,'add-a-new-employee.html')
    
def employee(request):
    data=models.retrieve_emp_data(user_id)
    return render(request,'employees.html',{'data':data})

def dashboard(request):
    no_of_employee = models.retreive_no_of_employee(user_id)
    # no_of_employee=10
    # models.create_table()
    # models.insert_data()
    # graphs.bar_char()
    return render(request,'dashboard.html',{'total_employees':no_of_employee[0]})

def employee_added(request):
    return render(request,'employee-added.html')
def employee_details(request):
    return render(request,'view-employee-profile.html')
def meeting_shcheduler(request):
    return render(request,'meeting-scheduler.html')
def add_new_meeting(request):
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        wit = request.POST.get('with')
        link = request.POST.get('link')
        data=models.retreive_meeting_data()
        length = len(data)
        for i in range(length):
            if time == data[i][0]:
                return render(request,'add-a-new-meeting.html')
        models.insert_data_meeting(title,date,time,wit,link,user_id)
        # print(fullname,email,company,contact,country)
        return HttpResponseRedirect('meeting-added')
    else:
        return render(request,'add-a-new-meeting.html')
    
def add_new_contact(request):
    if request.method == "POST":
        fullname = request.POST.get('client-name')
        email = request.POST.get('email')
        company = request.POST.get('comp-name')
        contact = request.POST.get('contact')
        country = request.POST.get('country')
        stage = request.POST.get('stg')
        status = request.POST.get('sts')
        newold = request.POST.get('new')
        data=models.retreive_data_client()
        length = len(data)
        for i in range(length):
            if email == data[i][0]:
                return render(request,'add-a-new-contact.html')
        models.insert_data_client(fullname,contact,email,company,status,stage,newold,user_id,country)
        # print(fullname,email,company,contact,country)
        return HttpResponseRedirect('contact-added')
    else:
        return render(request,'add-a-new-contact.html')
def contact_added(request):
    return render(request,'contact-added.html')
def project(request):
    return render(request,'projects.html')
def add_new_project(request):
     if request.method == "POST":
        project = request.POST.get('project')
        # assi= request.POST.get('assi')
        due = request.POST.get('dud')
        start = request.POST.get('std')
        status = request.POST.get('sts')
        # data=models.retreive_meeting_data()
        # length = len(data)
        # for i in range(length):
        #     if time == data[i][0]:
        #         return render(request,'add-a-new-meeting.html')
        models.insert_data_projects(project,start,due,status,user_id)
   
        return HttpResponseRedirect('project-added')
     else:
        return render(request,'add-a-new-project.html')
def project_added(request):
    return render(request,'project-added.html')
def meeting_added(request):
    return render(request,'meeting-added.html')
def project_details(request):
    return render(request,'projects-view-details.html')
def leads_pipeline(request):
    return render(request,'leads-pipeline.html')