from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Count, Case, When, Value, IntegerField, Q, F, ExpressionWrapper
from django.db.models.functions import ExtractMonth
from datetime import date, timedelta

class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_email = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[^@]+@[^@]+\.[^@]+$',
                message='Enter a valid email address.'
            )
        ]
    )
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'

class Client(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255)
    c_phone_no = models.CharField(max_length=255)
    c_email = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[^@]+@[^@]+\.[^@]+$',
                message='Enter a valid email address.'
            )
        ]
    )
    company_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    stage = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'clients'

class Project(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=255)
    due_date = models.DateField()
    starting_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=100, default='pending')

    class Meta:
        db_table = 'tasks'
        unique_together = (('project', 'task_id'),)

class Meeting(models.Model):
    m_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    m_time = models.TimeField()
    zoom_link = models.CharField(max_length=100)
    meetin_date = models.DateField()  # Note the typo in field name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'meetings'

class Employee(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    e_phone_no = models.CharField(max_length=255)
    e_email = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[^@]+@[^@]+\.[^@]+$',
                message='Enter a valid email address.'
            )
        ]
    )
    date_of_hiring = models.DateField()
    gender = models.CharField(max_length=255)
    salary = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=10)

    class Meta:
        db_table = 'employees'

class Assigned(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'assigned'
        unique_together = (('project', 'emp'),)
        
# User-related functions
def insert_data_user(name, email, password):
    User.objects.create(u_name=name, u_email=email, password=password)

def retreive_data_user():
    return list(User.objects.values_list('u_email', 'password', 'u_id'))

# Employee-related functions
def retrieve_emp_data(user_id):
    return list(Employee.objects.filter(user_id=user_id).values_list(
        'e_name', 'designation', 'e_phone_no', 'assigned__project__p_name'
    ))

def retreive_data_employee():
    return list(Employee.objects.values_list('e_email', flat=True))

def insert_data_employee(name, designation, phone, email, gender, country, salary, user_id):
    user = User.objects.get(u_id=user_id)
    Employee.objects.create(
        e_name=name,
        designation=designation,
        e_phone_no=phone,
        e_email=email,
        gender=gender,
        country=country,
        salary=salary,
        user=user,
        date_of_hiring=date.today()
    )

def retreive_no_of_employee(user_id):
    count = Employee.objects.filter(user_id=user_id).count()
    return (count,)

def emphired_thismonth(user_id):
    thirty_days_ago = date.today() - timedelta(days=30)
    count = Employee.objects.filter(
        user_id=user_id,
        date_of_hiring__gte=thirty_days_ago
    ).count()
    return (count,)

def retreive_ename(user_id):
    return list(Employee.objects.filter(user_id=user_id).values_list('e_name', flat=True))

# Project-related functions
def retreive_projects(user_id):
    projects = Project.objects.filter(user_id=user_id, client__user_id=user_id)
    assigned = Assigned.objects.filter(project__in=projects).select_related('project', 'emp', 'project__client')
    data = []
    for assign in assigned:
        data.append((
            assign.project.p_name,
            assign.project.client.c_name,
            assign.emp.e_name,
            assign.project.due_date
        ))
    return data

def retreive_data_projects(user_id):
    return list(Project.objects.filter(user_id=user_id).values_list('p_name', flat=True))

def insert_data_projects(name, client_name, due, tasks, assigned_emp_name, user_id):
    client = Client.objects.get(c_name=client_name, user_id=user_id)
    employee = Employee.objects.get(e_name=assigned_emp_name, user_id=user_id)
    project = Project.objects.create(
        p_name=name,
        starting_date=date.today(),
        due_date=due,
        user_id=user_id,
        client=client
    )
    Assigned.objects.create(project=project, emp=employee)
    for task_name in tasks:
        Task.objects.create(project=project, task_name=task_name)

def project_progress(user_id):
    projects = Project.objects.filter(user_id=user_id).annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__status='completed'))
    ).annotate(
        progress_percentage=Case(
            When(total_tasks=0, then=0),
            default=ExpressionWrapper(
                F('completed_tasks') * 100 / F('total_tasks'),
                output_field=IntegerField()
            )
        )
    ).values_list('p_id', 'progress_percentage')
    return list(projects)

def project_progress_name(user_id):
    projects = Project.objects.filter(user_id=user_id).annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__status='completed'))
    ).annotate(
        progress_percentage=Case(
            When(total_tasks=0, then=0),
            default=ExpressionWrapper(
                F('completed_tasks') * 100 / F('total_tasks'),
                output_field=IntegerField()
            )
        )
    ).values_list('p_name', 'progress_percentage')
    return list(projects)

def projects_yearly(user_id, year):
    queryset = Project.objects.filter(
        user_id=user_id,
        starting_date__year=year
    ).annotate(
        month=ExtractMonth('starting_date')
    ).values('month').annotate(
        project_count=Count('p_id')
    ).order_by('month')
    data = [(entry['month'], entry['project_count']) for entry in queryset]
    return data

def project_monthly(user_id):
    current_month = date.today().month
    current_year = date.today().year
    count = Project.objects.filter(
        user_id=user_id,
        starting_date__month=current_month,
        starting_date__year=current_year
    ).count()
    return (count,)

# Client-related functions
def retreive_email_client():
    return list(Client.objects.values_list('c_email', flat=True))

def insert_data_client(name, phone, email, company, status, stage, user_id, country):
    user = User.objects.get(u_id=user_id)
    Client.objects.create(
        c_name=name,
        c_phone_no=phone,
        c_email=email,
        company_name=company,
        status=status,
        stage=stage,
        user=user,
        country=country
    )

def retreive_contacts_details(user_id):
    return list(Client.objects.filter(user_id=user_id, status='active').values_list(
        'c_name', 'c_email', 'c_phone_no', 'company_name'
    ))

def retreive_cname(user_id):
    return list(Client.objects.filter(user_id=user_id).values_list('c_name', flat=True))

def retreive_prospects(user_id):
    return list(Client.objects.filter(
        user_id=user_id,
        status='pending',
        stage='prospect'
    ).values_list('c_name', 'c_email', 'company_name'))

def retreive_leads(user_id):
    return list(Client.objects.filter(
        user_id=user_id,
        status='pending',
        stage='Qualified lead'
    ).values_list('c_name', 'c_email', 'company_name'))

def retreive_calldone(user_id):
    return list(Client.objects.filter(
        user_id=user_id,
        status='pending',
        stage='call done'
    ).values_list('c_name', 'c_email', 'company_name'))

def retreive_cwon(user_id):
    return list(Client.objects.filter(
        user_id=user_id,
        status='pending',
        stage='client won'
    ).values_list('c_name', 'c_email', 'company_name'))

def update_client_stage(stage, client_name, user_id):
    Client.objects.filter(c_name=client_name, user_id=user_id).update(stage=stage)

def update_client_status(status, client_name, user_id):
    Client.objects.filter(c_name=client_name, user_id=user_id).update(status='active', stage=status)

# Meeting-related functions
def retreive_meeting_data(user_id):
    return list(Meeting.objects.filter(user_id=user_id).values_list('m_time', 'meetin_date'))

def retrieve_meetings(user_id):
    return list(Meeting.objects.filter(user_id=user_id).select_related('client').order_by(
        'meetin_date', 'm_time'
    ).values_list('title', 'meetin_date', 'm_time', 'client__c_name', 'zoom_link')[:3])

def insert_data_meeting(title, mtg_date, time, client_name, link, user_id):
    client = Client.objects.get(c_name=client_name, user_id=user_id)
    Meeting.objects.create(
        title=title,
        meetin_date=mtg_date,
        m_time=time,
        zoom_link=link,
        user_id=user_id,
        client=client
    )

def delete_prev_meeting(user_id):
    Meeting.objects.filter(user_id=user_id, meetin_date__lt=date.today()).delete()