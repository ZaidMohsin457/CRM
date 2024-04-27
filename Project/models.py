from django.db import connection

# Create your models here.
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
                create table if not exists users
                (
                    u_id serial primary key,
                    u_name varchar(255),
                    u_email varchar(255),
                    constraint email_format_check check (u_email like '%_@__%.__%'),
                    password varchar(255)
                );
                
                create table if not exists clients
                (
                    c_id serial primary key,
                    c_name varchar(255),
                    c_phone_no varchar(255),
                    c_email varchar(255),
                    constraint email_format_check check (c_email like '%_@__%.__%'),
                    company_name varchar(255),
                    status varchar(255),
                    stage varchar(255),
                    new_or_old varchar(255),
                    country varchar(50),
                    user_id int,
                    foreign key(user_id) references users(u_id)
                );
                
                create table if not exists projects
                (
                    p_id serial primary key,
                    p_name varchar(255),
                    due_date date,
                    starting_date date,
                    user_id int,
                    client_id int,
                    foreign key(user_id) references users(u_id),
                    foreign key(client_id) references clients(c_id)
                );
                
                create table if not exists tasks
                (
                    task_id serial,
                    project_id int,
                    task_name varchar(255),
                    t_status varchar(100) default 'pending',
                    foreign key(project_id) references projects(p_id),
                    primary key(project_id,task_id) 
                );
                create table if not exists meetings
                (
                    m_id serial primary key,
                    title varchar(255),
                    m_time time,
                    zoom_link varchar(100) not null ,
                    meetin_date date,
                    user_id int,
                    client_id int,
                    foreign key (user_id) references users(u_id),
                    foreign key(client_id) references clients(c_id)
                );
                
                create table if not exists employees
                (
                    e_id serial primary key,
                    e_name varchar(255),
                    designation varchar(255),
                    e_phone_no varchar(255),
                    e_email varchar(255),
                    constraint email_format_check check (e_email like '%_@__%.__%'),
                    gender varchar(255),
                    salary int,
                    user_id int,
                    country varchar(10),
                    foreign key(user_id) references users(u_id)
                );
                
                create table if not exists assigned
                (
                    project_id int,
                    emp_id int,
                    primary key(project_id,emp_id),
                    foreign key(project_id) references projects(p_id),
                    foreign key(emp_id) references employees(e_id)
                );
        """)
def insert_data_user(name,email,password):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO users (u_name,u_email,password) VALUES (%s,%s,%s);" ,[name,email,password])  
        
def retreive_data_user():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u_email,password,u_id FROM users;
        """)
        data = cursor.fetchall()
    return data



def retrieve_emp_data(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT e.e_name, e.designation, e_phone_no, p.p_name 
            FROM employees e
            LEFT JOIN assigned a ON e.e_id = a.emp_id
            LEFT JOIN projects p ON p.p_id = a.project_id
            where e.user_id=%s
            GROUP BY e.e_name, e.designation, e_phone_no, p.p_name;
        """,[user_id])
        data = cursor.fetchall()
    return data

def retreive_data_employee():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e_email from employees;
        """)
        data = cursor.fetchall()
    return data

def insert_data_employee(name,designation,phone,email,gender,country,salary,user_id):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO employees (e_name,designation,e_phone_no,e_email,gender,country,salary,user_id,date_of_hiring) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,current_date);" ,[name,designation,phone,email,gender,country,salary,user_id])
        
def retreive_no_of_employee(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            select count(e_id) from employees where user_id=%s;
        """,[user_id])
        data = cursor.fetchone()
    return data  
def retrieve_no_of_projects_this_month(user_id):
     with connection.cursor() as cursor:
        cursor.execute("""with mid as (select count(p.p_id) from projects p , tasks t where  p.p_id=t.project_id  and user_id=%s and
                       Current_date - p.starting_date between 0 and 30  group by p.p_id,t.status having status='Completed')
                       select count(*) from mid;""",[user_id])
        data=cursor.fetchone()
        return data
    
def emphired_thismonth(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""select count(e_id)from employees 
                        where  user_id =%s and current_date - date_of_hiring between 0 and 30;""",[user_id])
        data=cursor.fetchone()
        return data

def delasmade_this_month(user_id):
     with connection.cursor() as cursor:
        cursor.execute("""with res as(select count(*) as con from projects p , clients c where p.client_id=c.c_id and p.user_id=%s and
                       current_date - p.starting_date between 0 and 30 group by c.c_id having c.stage='Customer') 
                       select sum(con) from res;""",[user_id])
        data=cursor.fetchone()
        return data



def retreive_projects(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            select p.p_name,c.c_name,e.e_name, p.due_date from projects p, clients c ,employees e,assigned a where p.user_id=%s and p.client_id=c.c_id and c.user_id=p.user_id and a.project_id=p.p_id and a.emp_id=e.e_id;
        """,[user_id])
        data = cursor.fetchall()
    return data

def retreive_data_projects(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p_name from projects where user_id=%s;
        """,[user_id])
        data = cursor.fetchall()
    return data

def insert_data_projects(name,client,due,tasks,assigned,user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT c_id FROM clients WHERE c_name=%s AND user_id=%s;",[client,user_id])
        cli_id = cursor.fetchone()
        cursor.execute("SELECT e_id FROM employees WHERE e_name=%s AND user_id=%s;",[assigned,user_id])
        emp_id = cursor.fetchone()
        cursor.execute(" INSERT INTO projects (p_name,starting_date,due_date,user_id,client_id) VALUES (%s,current_date,%s,%s,%s);"
                       ,[name,due,user_id,cli_id])
        cursor.execute("SELECT p_id FROM projects WHERE p_name=%s AND user_id=%s;",[name,user_id])
        proj = cursor.fetchone()
        cursor.execute(" INSERT INTO assigned(project_id,emp_id) VALUES (%s,%s);",[proj,emp_id])
        for i in tasks:
            cursor.execute(" INSERT INTO tasks (project_id,task_name) VALUES (%s,%s);",[proj,i]) 
       
def project_progress(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
            projects.p_id AS project_id,
            CASE 
                WHEN COUNT(tasks.task_id) = 0 THEN 0
                ELSE (COUNT(CASE WHEN tasks.t_status = 'completed' THEN 1 END) * 100) / COUNT(tasks.task_id)
            END AS progress_percentage
            FROM 
                projects
            LEFT JOIN 
                tasks ON projects.p_id = tasks.project_id
                WHERE projects.user_id=%s
            GROUP BY 
                projects.p_id;
        """,[user_id])
        data = cursor.fetchall()
    return data  

def project_progress_name(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
            projects.p_name AS project_name,
            CASE 
                WHEN COUNT(tasks.task_id) = 0 THEN 0
                ELSE (COUNT(CASE WHEN tasks.t_status = 'completed' THEN 1 END) * 100) / COUNT(tasks.task_id)
            END AS progress_percentage
            FROM 
                projects
            LEFT JOIN 
                tasks ON projects.p_id = tasks.project_id
                WHERE projects.user_id=%s
            GROUP BY 
                projects.p_id;
        """,[user_id])
        data = cursor.fetchall()
    return data  

def projects_yearly(user_id,year):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXTRACT(MONTH FROM starting_date) AS month,
            COUNT(*) AS project_count
            FROM projects
            where user_id=%s and EXTRACT(YEAR FROM starting_date)=%s
            GROUP BY EXTRACT(MONTH FROM starting_date)
            ORDER BY EXTRACT(MONTH FROM starting_date);
        """,[user_id,year])
        data = cursor.fetchall()
    return data

def project_monthly(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
                       select
                        COUNT(*) AS project_count
                        FROM projects
                        where user_id=%s and EXTRACT(MONTH FROM starting_date)=EXTRACT(MONTH FROM current_date)
                        GROUP BY EXTRACT(MONTH FROM starting_date)
                        ORDER BY EXTRACT(MONTH FROM starting_date);
        """,[user_id])
        data = cursor.fetchone()
    return data


def retreive_data_client():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c_email from clients;
        """)
        data = cursor.fetchall()
    return data

def insert_data_client(name,phone,email,company,status,stage,new,user_id,country):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO clients (c_name,c_phone_no,c_email,company_name,status,stage,new_or_old,user_id,country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                       ,[name,phone,email,company,status,stage,new,user_id,country])
        
def retreive_contacts_details(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            select c_name,c_email,c_phone_no,company_name from clients where user_id=%s;
        """,[user_id])
        data = cursor.fetchall()
    return data
        
   
        
def retreive_meeting_data(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""Select m_time,meeting_date from meetings where user_id=%s;""",[user_id])  
        data = cursor.fetchall() 
    return data    

def retrieve_meetings(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            select m.title, m.meeting_date, m.m_time, c.c_name, m.zoom_link from meetings m, clients c where m.user_id=%s and m.client_id=c.c_id
            order  by m.meeting_date asc, m.m_time asc
            limit 3;
        """,[user_id])
        data = cursor.fetchall()
    return data
def insert_data_meeting(title,date,time,withm,link,user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT c_id FROM clients WHERE c_name=%s AND user_id=%s;",[withm,user_id])
        cli_id = cursor.fetchone()
        cursor.execute(" INSERT INTO meetings (title,meeting_date,m_time,client_id,zoom_link,user_id) VALUES (%s,%s,%s,%s,%s,%s);"
                       ,[title,date,time,cli_id,link,user_id])
        
       