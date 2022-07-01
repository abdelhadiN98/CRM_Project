from asyncio.windows_events import NULL
from multiprocessing import context
from turtle import title
from django.shortcuts import redirect, render

from login_updated_app.models import Employee , Customer , Service

# render the services page which employee can see after login

def service_page(request):
    if not 'employee_id' in request.session:
        return redirect('/')
    else :
        this_employee = Employee.objects.get(id=request.session['employee_id'])
        # print(this_user.id)
        context={
            'this_employee' : this_employee,
            'all_services' : Service.objects.all()
        }
        return render(request , 'welcome.html' , context)

# method to add a service 

def create_service(request):
    this_employee = Employee.objects.get(id=request.session['employee_id'])
    # if this_employee.is_admin:
    Service.objects.create(
        title = request.POST['title'],
        desc = request.POST['description'],
        managed_by = Employee.objects.get(id=request.session['employee_id'])
    )
    
    return redirect('/services')

# method to render the service details page

def service_details(request , service_id):
    this_employee = Employee.objects.get(id=request.session['employee_id'])
    this_service = Service.objects.get(id = service_id)
    all_customers = Customer.objects.all()
    this_service_customers = this_service.customers_have_servives.all()
    context = {
        'this_service' : this_service,
        'all_customers' : all_customers,
        'this_service_customers' : this_service_customers,
        'this_employee' : this_employee,

    }
    return render(request , 'serviceDetails.html' ,context)

# method to delete the service by employee

def delete_service(request , service_id):
    this_service = Service.objects.get(id = service_id)
    this_service.delete()
    return redirect('/services')

# method to render the update page which contains a form for services

def update_service(request ,service_id ):
    this_service = Service.objects.get(id = service_id)
    context = {
        'this_service' : this_service,
    }
    return render(request , 'updateService.html' , context)

# method for update the information for the service 
def update_service_info(request , service_id):
    this_service = Service.objects.get(id = service_id)
    this_service.title = request.POST['update_title']
    this_service.desc = request.POST['update_description']
    this_service.save()
    return redirect('/services')

# method to render a page which contains the form creation for customers

def create_customer(request):
    return render(request , 'customerForm.html')

# method to create the customer with his\her information and store these info in database

def addCustomer(request):
    Customer.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        managed_by = Employee.objects.get(id=request.session['employee_id'])
    )
    return redirect('/services')

# method to render a page contains my information (my profile)

def myProfile(request):
    current_employee = Employee.objects.get(id = request.session['employee_id'])
    context={
        'current_employee' : current_employee,
    }
    return render(request , 'myProfile.html' , context)

# method to update my information 

def update_info(request):
    current_employee = Employee.objects.get(id=request.session['employee_id'])
    current_employee.first_name = request.POST['update_first_name']
    current_employee.last_name = request.POST['update_last_name']
    current_employee.email = request.POST['update_email']
    current_employee.save()
    return redirect('/services')

    # method to add this customer to this service

def addCsutomerToService(request , service_id):
    this_service = Service.objects.get(id = service_id)
    this_customer = request.POST['customer']
    this_service.customers_have_servives.add(this_customer)
    return redirect(f'/service/details/{service_id}')

    # method to delete this service from this customer
def removeCsutomerToService(request , service_id , customer_id):
    this_service = Service.objects.get(id = service_id)
    this_customer = Customer.objects.get(id = customer_id)
    this_service.customers_have_servives.remove(this_customer)
    return redirect(f'/service/details/{service_id}')

# method to logout from the application
def logout(request):
    del request.session['employee_id']
    return redirect('/')

# method to render a page which contains a list of all customers :

def allCustomers(request):
    all_customers = Customer.objects.all()
    context={
        'all_customers' : all_customers,
    }
    return render(request , 'allCustomers.html' , context)

# method to delete the customer from database 
def deleteCustomer(request , customer_id) :
    this_customer = Customer.objects.get(id = customer_id)
    this_customer.delete()
    return redirect('/allCustomers')