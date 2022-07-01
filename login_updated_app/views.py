from django.shortcuts import render,redirect 
from .models import Employee
import bcrypt
from django.contrib import messages

def main(request):
    return render(request ,'index.html')


# method for registration and redirect to main page:
def register(request):
    errors = Employee.objects.register_validator(request.POST)
    request.session['coming_from'] = 'register'
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif len(Employee.objects.filter(email=request.POST['email']))>0:
        messages.error(request, "This email already exist !")
    else:
        password = request.POST['password']
        confirm_pass = request.POST['confirm_password']
        if password == confirm_pass :
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            print(Employee.objects.count())
            Employee.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
                is_admin = True if Employee.objects.count() == 0 else False
                )
            
            this_employee = Employee.objects.get(email=request.POST['email'])
            # print("hiiiii")
            # print(Employee.objects.count())
            # if Employee.objects.count() == 1 :
            #     this_employee.is_admin == True
            #     this_employee.save()
            
            request.session['employee_id'] = this_employee.id
            
        # messages.success(request, "User successfully registerd")
        # redirect to success
        return redirect('/services')

def login(request):
    errors = Employee.objects.login_validator(request.POST)
    request.session['coming_from'] = 'login'
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    if not Employee.objects.filter(email=request.POST['login_email']):
        messages.error(request, "not signed in! register now")
        return redirect('/')
    else:
        this_employee=Employee.objects.get(email=request.POST['login_email'])
        if this_employee:
            if bcrypt.checkpw(request.POST['login_password'].encode(), this_employee.password.encode()):
                request.session['employee_id'] = this_employee.id
                request.session['first_name'] = this_employee.first_name
                return redirect('/services')
            else:
                messages.error(request, "the password is incorrect")
                return redirect("/")

