from email import errors
from django.shortcuts import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
import requests

from .models import *
from mywebsite.models import *


def company_job(request):
    print(request.user.email)
    company = Company.objects.get(official_email = request.user.email)
    if request.method == "POST":
            jobpost_name = request.POST.get('jobpost_name')
            jobpost_phoneno = request.POST.get('jobpost_phoneno')
            jobpost_email = request.POST.get('jobpost_email')
            jobpost_designation = request.POST.get('jobpost_designation')
            job_title = request.POST.get('job_title')
            job_workplace = request.POST.get('job_workplace')
            job_location = request.POST.get('job_location')
            job_type = request.POST.get('job_type')
            job_no_opening = request.POST.get('job_no_opening')
            job_salary = request.POST.get('job_salary')
            job_skills = request.POST.get('job_skills')
            # description = request.POST.get('description')
            
            errors = []
            if not jobpost_name or not jobpost_phoneno or not jobpost_email or not job_title:
                # return HttpResponse("Error: Required fields are missing.", status=400)
                print()
                errors.append("Error: Required fields are missing.")  
                
                if errors:
                    for error in errors:
                        messages.error(request, error)
            else:
                # Create and save the JobPost object to the database
                api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCNQc9p6c2_fYszrGsRIKlzuna5v6oOxtI'
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [
                            {"text": f"write output in json format"},
                            {"text": f"JD Type: {job_title}"},
                            {"text": "Experience: 3-5 years"},
                            {"text": f"Skills: {job_skills}"},
                            {"text": f"Salary Range: {job_salary}"},
                            {"text": f"Job Type: {job_type}"},
                            {"text": f"Location: {job_location}"},
                            {"text": "Length: Concise"},
                            {"text": "Time Period: {job_type}"},
                            {"text": "Now, based on the above points, write a detailed 500-word job description covering responsibilities, qualifications, preferred skills, company culture, and benefits."}
                        ]
                    }]
                }
                
                # Make the API request
                response = requests.post(api_url, headers=headers, json=data)
                print(response.status_code)
                print(response.text)
                
                if response.status_code == 200:
                    response_data = response.json()
                    print(response_data)
                    try:
                        description = response_data['candidates'][0]['content']['parts'][0]['text']
                    except (KeyError, IndexError) as e:
                        description = 'No description available.'
                        messages.error(request, "Failed to extract job description from API response.")
                        # Extract the generated description from the API response
                else:
                    description = 'Failed to generate description.'
                    messages.error(request, "Failed to generate job description from API.")
                
                # Create and save the JobPost object to the database
                
                print("start object created")
                job = Job.objects.create(
                    jobpost_name=jobpost_name,
                    jobpost_phoneno=jobpost_phoneno,
                    jobpost_email=jobpost_email,
                    jobpost_designation=jobpost_designation,
                    job_title=job_title,
                    job_workplace=job_workplace,
                    job_location=job_location,
                    job_type=job_type,
                    job_no_opening=job_no_opening,
                    job_salary=job_salary,
                    job_skills=job_skills,
                    company=company,
                    description=description,
                )
                job.save()
                print("end object created")
            messages.success(request,"Company registration Sucessfully!")
    
    return render(request,"job_post.html")



def company_profile(request):
    print(request.user.email)
    company = Company.objects.get(official_email = request.user.email)

    if request.method == "POST":
        name = request.POST.get('company_name')
        phone_number = request.POST.get('company_phone')
        website = request.POST.get('company_url')
        address = request.POST.get('company_address',"")
        industry = request.POST.get('company_work')
        number_of_employees = request.POST.get('num_employees')
        company_logo = request.POST.get('company_logo')
        
        errors = []
        if not phone_number.isdigit():
            errors.append("Phone number must contain only digits.")
        if len(phone_number)<10:
            errors.append("Phone number must be at least 10 digits.")
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            company.name=name
            company.phone_number=phone_number
            company.website=website
            company.address=address
            company.industry=industry
            company.number_of_employees=number_of_employees
            company.company_logo=company_logo
            company.save()
        
        
    context={
        "company":company,
    }
    return render(request,"company_profile.html",context = context)

from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Company_Register
from django.contrib.auth.hashers import make_password  # For hashing the password


def company_register(request):
    
    if request.method == "POST":
        name = request.POST.get('company_name')
        phone_number = request.POST.get('company_phone')
        official_email = request.POST.get('office_email')
        website = request.POST.get('company_url')
        address = request.POST.get('company_address')
        industry = request.POST.get('company_work')
        number_of_employees = request.POST.get('num_employees')
        password = request.POST.get('password')
        print(name , phone_number , official_email , website , address , industry , number_of_employees , password)
        
        errors = []
        if not name or not phone_number or not official_email or not website or not address or not industry or not number_of_employees or not password:
            errors.append("All Fields marked with * are required. ")
        # TODO : Later validation
        # if not phone_number.isdigit():
        #     errors.append("Phone number must contain only digits.")
        # if len(phone_number)<10:
        #     errors.append("Phone number must be at least 10 digits.")
        # if Company.objects.filter(official_email=official_email).exists():
        #     errors.append("Email is already registered.")
        # if "@gmail.com" in official_email:
        #     errors.append("Gmail addresses are not allowed for the company email.")
        # if len(password) < 8:
        #     errors.append("Password must be at least 8 characters long.")  
        if Company.objects.filter(official_email=official_email).exists():
            errors.append("Email is already registered.")
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            hashed_password = make_password(password)
 
            company = Company.objects.create(
                name = name,
                phone_number=phone_number,
                official_email=official_email,
                website=website,
                address=address,
                industry=industry,
                number_of_employees=number_of_employees,
                password=hashed_password,
            )
            if not User.objects.filter(email=official_email+"+company").exists():
                # Add the user to the User table
                user = User.objects.create_user(
                    username= official_email+"+company",  # Use email as the username
                    email=official_email,
                    password=password,
                )
                print("User created:", user.username)
                
                try:
                    company_group = Group.objects.get(name="Company")  # Fetch the "Company" group
                    user.groups.add(company_group)  # Add the user to the group
                    
                except Group.DoesNotExist:
                    Group.objects.create(name="Company")  # Create the group if it doesn't exist
                    print("The 'Company' group does not exist. Please create it in the Admin panel.")
                    company_group = Group.objects.get(name="Company")  # Fetch the "Company" group
                    user.groups.add(company_group)  # Add the user to the group
                user.save()  # Save the user instance

            messages.success(request, "User added to the system.")
            messages.success(request,"Company registration Sucessfully!")
        return redirect('company_register')
    return render(request,'company_register.html')

def company_login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get('password')
        # TODO: later validation
        if "@gmail.com" in email and False:
            messages.error(request,"Its not be a official email id")
            return redirect('company_login')
        else:
            emailid = email

        user1 = authenticate(request,username= emailid+"+company" , password = password)

        if user1 is not None:
            login(request,user1)
            return redirect('company_front')
        else:
            messages.error(request,"Invalid email id or password")
            return redirect('company_login')
        
    return render(request,'company_login.html')


def company_forgot_password(request):
    context= {"step": "1"}
    
    if request.method == "POST":
        step=request.POST.get('step', '1')
        print("Step:", step)
        email = request.POST.get('email')
        if step == "2":
            if not Company.objects.filter(official_email=email).exists():
                context = {'step': "1"}
                messages.error(request, "Email not found.")
            else:
                messages.success(request, "OTP has been sent to your email.")
                context = {'step': "2", 'email': email}
        if step == "3":
            action=request.POST.get('action')
            if action == "resend_otp":
                if not Company.objects.filter(official_email=email).exists():
                    messages.error(request, "Email not found.")
                # Logic to resend OTP goes here
                messages.success(request, "OTP has been resent to your email.")
                context = {'step': "2", 'email': email}
            else:
                otp = request.POST.get('otp')
                if not otp:
                    messages.error(request, "OTP is required.")
                    context = {'step': "2", 'email': email}
                if not Company.objects.filter(official_email=email).exists():
                    messages.error(request, "Email not found.")
                    context = {'step': "2", 'email': email}
                if otp == "123456":  # Replace with actual OTP validation logic
                    messages.success(request, "OTP verified successfully. You can now reset your password.")
                    context = {'step': "3", 'email': email}
        if step == "4":
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if not password or not cpassword:
                messages.error(request, "Both password fields are required.")
                context = {'step': "3", 'email': email}
            elif password != cpassword:
                messages.error(request, "Passwords do not match.")
                context = {'step': "3", 'email': email}
            elif not Company.objects.filter(official_email=email).exists():
                messages.error(request, "Email not found.")
                context = {'step': "3", 'email': email}
            else:
                try:
                    user = User.objects.get(username=email+"+company")
                    user.set_password(password)  # Hash the new password
                    user.save()
                    messages.success(request, "Password changed successfully. You can now login.")
                    return redirect('company_login')  # Redirect to login page
                except Company.DoesNotExist:
                    messages.error(request, "Company not found.")
                    context = {'step': "1"}

    return render(request, 'company_forgot_password.html',context)


def company_front(request):
    print(request.user.email)
    user_email = request.user.email
    job = Job.objects.filter(company__official_email=user_email)
    print(job)
    return render(request, 'company_front.html',{"job":job})

from django.shortcuts import render, get_object_or_404
from .models import Job

def card_detail(request, unique_number):
    # Retrieve the specific card using the unique_id
    job = get_object_or_404(Job, unique_number=unique_number)
    # Render the template with the job details
    return render(request, 'card_detail.html', {'job': job})