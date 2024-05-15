from django.shortcuts import render,HttpResponseRedirect
from Project import models
from Project import graphs
from django.utils import timezone
import re
user_id=1
def modify(id):
    global user_id
    user_id=id
def index(request):
    models.create_table()
    return render(request,'desktop-1.html')
def login(request):#done
    message=None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data=models.retreive_data_user()
        if len(data)==0:
            message="No User Registered .. Please Sign Up First"
            return render(request,'login-page.html',{'message':message})
        if email == data[0][0] and password == data[0][1]:
            modify(data[0][2])
            return HttpResponseRedirect("home")
        else:
            message="Invalid Email or Password .. Try Again"
            return render(request,'login-page.html',{'message':message})
    else:
        return render(request,'login-page.html')
    
def signup(request):#done
    message=None
    if request.method == "POST":
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        if email.find('@')==-1 or email.find('.')==-1:
            message="Invalid Email .. Please Enter a valid Email"
            return render(request,'sign-up-page.html',{'message':message})
        password = request.POST.get('password')
        if len(password)==0:
            message="Password cannot be empty .. Please Enter a password"
            return render(request,'sign-up-page.html',{'message':message})
        data=models.retreive_data_user()
        length = len(data)
        if length==0:
            models.insert_data_user(fullname,email,password)
            return HttpResponseRedirect('login')
        for i in range(length):
            if email == data[i][0]:
                message="Email already registered.. Try another Email"
                return render(request,'sign-up-page.html',{'message':message})
        models.insert_data_user(fullname,email,password)
        return HttpResponseRedirect('login')
    else:
        return render(request,'sign-up-page.html')
    
def dashboard(request):
    no_of_employee = models.retreive_no_of_employee(user_id)
    no_of_employee_hired_this_month = models.emphired_thismonth(user_id)
    year=timezone.now().year
    data=models.projects_yearly(user_id,year)
    graphs.projects_graph(data)
    data1=models.project_monthly(user_id)
    data2=models.project_progress_name(user_id)
    graphs.bar_char(data2)
    no_of_projects_this_month=models.project_monthly(user_id)
    return render(request,'dashboard.html',{'total_employees':no_of_employee,'proj':no_of_projects_this_month,'this_month':no_of_employee_hired_this_month,'deals':data1})



#Projects
def project(request):
    data=models.retreive_projects(user_id)
    present=timezone.now().date()
    diff=[]
    progress=models.project_progress(user_id)
    if len(data)==0:
        return render(request,'projects.html',{'data':data})
    for i in range(len(data)):
        rem=data[i][3]-present
        diff.append(rem.days)
    combined=zip(data,diff,progress)
    return render(request,'projects.html',{'data':combined})

def add_new_project(request):
    message=None
    if request.method == "POST":   
        project = request.POST.get('name')
        assigned= request.POST.get('employee')
        due = request.POST.get('duedate')
        client = request.POST.get('client')
        tasks = request.POST.get('tasks').split(',')
        data=models.retreive_data_projects(user_id)
        length = len(data)
        data1=models.retreive_cname(user_id)
        if client not in data1:
            message="Client Not Present .. Add Client First"
            return render(request,'add-a-new-project.html',{'message':message})
        if length==0:
            models.insert_data_projects(project,client,due,tasks,assigned,user_id)
            return HttpResponseRedirect('project-added')
        for i in range(length):
            if project == data[i][0]:
                message="Project Already Present .. Try Again"
                return render(request,'add-a-new-project.html',{'message':message})
        models.insert_data_projects(project,client,due,tasks,assigned,user_id)
        return HttpResponseRedirect('project-added')
    else:
        cnames=models.retreive_cname(user_id)
        enames=models.retreive_ename(user_id)
        return render(request,'add-a-new-project.html',{'clients':cnames,'employees':enames})

def project_added(request):
    return render(request,'project-added.html')



#Employee
def employee(request):#done
    data=models.retrieve_emp_data(user_id)
    merged_data = {}
    for item in data:
        name, designation, phone, project = item
        if name not in merged_data:
            merged_data[name] = {'designation': designation, 'phone': phone, 'projects': []}
        if project:
            merged_data[name]['projects'].append(project)
    final_result = [
        (name, details['designation'], details['phone'], ', '.join(details['projects']))
        for name, details in merged_data.items()
    ]
    return render(request,'employees.html',{'data':final_result})

def add_new_employee(request):#done
    message=None
    if request.method == "POST":
        name = request.POST.get('name')
        enames=models.retreive_ename(user_id)
        if name in enames:
            message="Employee Already Present .. Try adding another Employee"
            return render(request,'add-a-new-employee.html',{'message':message})
        designation = request.POST.get('designation')
        phone = request.POST.get('contact')
        email = request.POST.get('email')
        if email.find('@')==-1 or email.find('.')==-1: 
            message="Invalid Email .. Please Enter a valid Email"
            return render(request,'add-a-new-employee.html',{'message':message})
        gender = request.POST.get('gender')
        salary = int((request.POST.get('salary')),10)
        if salary<=0:
            message="Salary cannot be negative and zero .. Please Enter a valid salary"
            return render(request,'add-a-new-employee.html',{'message':message})
        coun = request.POST.get('country')
        data=models.retreive_data_employee()
        length = len(data)
        if length==0:
            models.insert_data_employee(name,designation,phone,email,gender,coun,salary,user_id)
            return HttpResponseRedirect('employee-added')
        for i in range(length):
            if email == data[i][0]:
                message="Employee Already Present .. Try adding another email"
                return render(request,'add-a-new-employee.html',{'message':message})
        models.insert_data_employee(name,designation,phone,email,gender,coun,salary,user_id)
        return HttpResponseRedirect('employee-added')
    else:
        return render(request,'add-a-new-employee.html')

def employee_added(request):
    return render(request,'employee-added.html')



#Meetings
def meeting_shcheduler(request):#done
    data=models.retreive_contacts_details(user_id)
    models.delete_prev_meeting(user_id)
    meetings=models.retrieve_meetings(user_id)
    now=None
    if len(meetings)==0:
        return render(request,'meeting-scheduler.html',{'data':data,'now':now,'meetings':meetings})
    if meetings[0][1] == timezone.now().date():
        now=meetings[0]
        meetings=meetings[1:]
    else:
        now=None
    return render(request,'meeting-scheduler.html',{'data':data,'now':now,'meetings':meetings})

def validate_time_format(input_time):
    pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
    if re.match(pattern, input_time):
        return True
    else:
        return False
def validate_date_format(input_date):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, input_date):
        return True
    else:
        return False
def add_new_meeting(request):#done
    message=None
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        if date < str(timezone.now().date()):
            message="Invalid Date .. Please Enter a Future Date"
            return render(request,'add-a-new-meeting.html',{'message':message})
        if not validate_date_format(date):
            message="Invalid Date Format .. Please Enter Date in YYYY-MM-DD format"
            return render(request,'add-a-new-meeting.html',{'message':message})
        time = request.POST.get('time')
        if not validate_time_format(time):
            message="Invalid Time Format .. Please Enter Time in HH:MM format"
            return render(request,'add-a-new-meeting.html',{'message':message})
        time = time + ":00"
        wit = request.POST.get('with')
        link = request.POST.get('link')
        data=models.retreive_meeting_data(user_id)
        length = len(data)
        if length==0:
            models.insert_data_meeting(title,date,time,wit,link,user_id)
            return HttpResponseRedirect('meeting-added')
        for i in range(length):
            if time == str(data[i][0]) and date == str(data[i][1]):
                message="Time slot not available ..Try Another Time Slot."
                return render(request,'add-a-new-meeting.html',{'message':message})
        models.insert_data_meeting(title,date,time,wit,link,user_id)
        return HttpResponseRedirect('meeting-added')
    else:
        cnames=models.retreive_cname(user_id)
        return render(request,'add-a-new-meeting.html',{'clients':cnames})

def meeting_added(request):
    return render(request,'meeting-added.html')



#Lead-Pipeline
def leads_pipeline(request):
    if request.method =="POST":
        option=request.POST.get('cstatus').split(',')
        if option[0]!="Confirmed":
            models.update_client_stage(option[0],option[1],user_id)
        else:
            models.update_client_status(option[0],option[1],user_id)
        return HttpResponseRedirect('leads-pipeline')
    else:
        prospects=models.retreive_prospects(user_id)
        leads=models.retreive_leads(user_id)
        cwon=models.retreive_cwon(user_id)
        call_done=models.retreive_calldone(user_id)
        return render(request,'leads-pipeline.html',{'prospects':prospects,'leads':leads,'cwon':cwon,'call_done':call_done}) 

def add_new_contact(request):#done
    message=None
    if request.method == "POST":
        fullname = request.POST.get('client-name')
        names=models.retreive_cname(user_id)
        if fullname in names:
            message="Contact Already Present .. Try Again"
            return render(request,'add-a-new-contact.html',{'message':message})
        email = request.POST.get('email')
        if email.find('@')==-1 or email.find('.')==-1:
            message="Invalid Email .. Please Enter a valid Email"
            return render(request,'add-a-new-contact.html',{'message':message})
        company = request.POST.get('comp-name')
        contact = request.POST.get('contact')
        country = request.POST.get('country')
        stage = request.POST.get('stg')
        status = request.POST.get('sts')
        # newold = request.POST.get('new')
        data=models.retreive_email_client()
        length = len(data)
        if length==0:
            models.insert_data_client(fullname,contact,email,company,status,stage,user_id,country)
            return HttpResponseRedirect('contact-added')
        for i in range(length):
            if email == data[i][0]:
                message="Contact Already Present .. Try Again"
                return render(request,'add-a-new-contact.html',{'message':message})
        models.insert_data_client(fullname,contact,email,company,status,stage,user_id,country)
        return HttpResponseRedirect('contact-added')
    else:
        return render(request,'add-a-new-contact.html')
    
def contact_added(request):
    return render(request,'contact-added.html')