from django.shortcuts import render,HttpResponseRedirect
from Project import models
from Project import graphs
from django.utils import timezone

# Create your views here.
user_id=1
def modify(id):
    global user_id
    user_id=id
def index(request):
    models.create_table()
    return render(request,'desktop-1.html')
def login(request):
    message=None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data=models.retreive_data_user()
        # print(email,password)
        if email == data[0][0] and password == data[0][1]:
            modify(data[0][2])
            return HttpResponseRedirect("home")
        else:
            message="Invalid Email or Password .. Try Again"
            return render(request,'login-page.html',{'message':message})
    else:
        return render(request,'login-page.html')
def signup(request):
    message=None
    if request.method == "POST":
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        data=models.retreive_data_user()
        length = len(data)
        for i in range(length):
            if email == data[i][0]:
                message="Email already registered.. Try another Email"
                return render(request,'sign-up-page.html',{'message':message})
        models.insert_data_user(fullname,email,password)
        # print(fullname,email,password)
        return HttpResponseRedirect('login')
    else:
        return render(request,'sign-up-page.html')
    

def add_new_employee(request):
    message=None
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
                message="Employee Already Present .. Try adding another email"
                return render(request,'add-a-new-employee.html',{'message':message})
        models.insert_data_employee(name,designation,phone,email,gender,coun,salary,user_id)
        return HttpResponseRedirect('employee-added')
    else:
        return render(request,'add-a-new-employee.html')
    
def employee(request):
    data=models.retrieve_emp_data(user_id)
    return render(request,'employees.html',{'data':data})

def employee_added(request):
    return render(request,'employee-added.html')
def project_added(request):
    return render(request,'project-added.html')
def meeting_added(request):
    return render(request,'meeting-added.html')
def contact_added(request):
    return render(request,'contact-added.html')

def add_new_meeting(request):
    message=None
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        time = time + ":00"
        wit = request.POST.get('with')
        link = request.POST.get('link')
        data=models.retreive_meeting_data(user_id)
        length = len(data)
        for i in range(length):
            # print(data[i][1],type(str(data[i][1])),date,type(date),date==str(data[i][1]))
            if time == str(data[i][0]) and date == str(data[i][1]):
                message="Time slot not available ..Try Another Time Slot."
                return render(request,'add-a-new-meeting.html',{'message':message})
        models.insert_data_meeting(title,date,time,wit,link,user_id)
        return HttpResponseRedirect('meeting-added')
    else:
        return render(request,'add-a-new-meeting.html')
    
    
def dashboard(request):
    no_of_employee = models.retreive_no_of_employee(user_id)
    no_of_employee_hired_this_month = models.emphired_thismonth(user_id)
    no_of_projects_this_month=models.retrieve_no_of_projects_this_month(user_id)
    # no_of_employee=10
    # models.create_table()
    # models.insert_data()
    # graphs.bar_char()
    return render(request,'dashboard.html',{'total_employees':no_of_employee[0],
                                            'this_month':no_of_employee_hired_this_month[0],
                                            'proj':no_of_projects_this_month[0]})

def employee_details(request):
    return render(request,'view-employee-profile.html')
def meeting_shcheduler(request):
    data=models.retreive_contacts_details(user_id)
    return render(request,'meeting-scheduler.html',{'data':data})
 
def add_new_contact(request):
    message=None
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
                message="Contact Alreday Present .. Try Again"
                return render(request,'add-a-new-contact.html',{'message':message})
        models.insert_data_client(fullname,contact,email,company,status,stage,newold,user_id,country)
        return HttpResponseRedirect('contact-added')
    else:
        return render(request,'add-a-new-contact.html')
def project(request):
    data=models.retreive_projects(user_id)
    present=timezone.now().date()
    diff=data[0][3]-present
    return render(request,'projects.html',{'data':data,'diff':diff.days})
def add_new_project(request):
     if request.method == "POST":
        project = request.POST.get('name')
        assigned= request.POST.get('employee')
        due = request.POST.get('duedate')
        client = request.POST.get('client')
        tasks = request.POST.get('tasks')
        models.insert_data_projects(project,client,due,tasks,assigned,user_id)
   
        return HttpResponseRedirect('project-added')
     else:
        return render(request,'add-a-new-project.html')
    
    
def project_details(request):
    return render(request,'projects-view-details.html')
def leads_pipeline(request):
    return render(request,'leads-pipeline.html')


    