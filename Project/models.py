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
                    user_id int,
                    foreign key(user_id) references users(u_id)
                );
                
                create table if not exists projects
                (
                    p_id serial primary key,
                    p_name varchar(255),
                    due_date date,
                    user_id int,
                    client_id int,
                    foreign key(user_id) references users(u_id),
                    foreign key(client_id) references clients(c_id)
                );
                
                create table if not exists tasks
                (
                    task_id int,
                    project_id int,
                    task_name varchar(255),
                    foreign key(project_id) references projects(p_id),
                    primary key(project_id,task_id) 
                );
                create table if not exists meetings
                (
                    m_id serial primary key,
                    title varchar(255),
                    m_time timestamp,
                    zoom_link varchar(100) not null ,
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
            SELECT u_email,password FROM users;
        """)
        data = cursor.fetchall()
    return data

def retrieve_emp_data():
    with connection.cursor() as cursor:
        cursor.execute("""
            select e.e_name,e.designation,e.e_phone_no from employees e ;
        """)
        data = cursor.fetchall()
    return data

def retreive_data_employee():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e_name,designation,e_phone_no,e_email,gender,country,salary from employees;
        """)
        data = cursor.fetchall()
    return data

def insert_data_employee(name,des,phone,mail,gen,coun,sal):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO employees (e_name,designation,e_phone_no,e_email,gender,country,salary) VALUES (%s,%s,%s,%s,%s,%s,%d);" ,[name,des,phone,mail,gen,coun,sal])