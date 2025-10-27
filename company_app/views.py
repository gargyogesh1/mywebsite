from email import errors
from django.shortcuts import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
import requests

from .models import *
from mywebsite.models import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Company_Register
from django.contrib.auth.hashers import make_password  # For hashing the password

from django.shortcuts import render, get_object_or_404
from .models import Job
from django.http import JsonResponse

# def card_detail(request, unique_number):
#     # Retrieve the specific card using the unique_id
#     job = get_object_or_404(Job, unique_number=unique_number)
#     print(job.description)
#     # Render the template with the job details
#     return render(request, 'job_detail.html', {'job': job})

import json, re
from django.shortcuts import render, get_object_or_404
from .models import Job


def company_job(request):
    print(request.user.email)
    company = Company.objects.get(official_email = request.user.email)
    print(company)
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
                            {"text": "Now, based on the above points, write a detailed 500-word job description covering responsibilities, qualifications, preferred skills, company culture, and benefits."},
                            {"text": "provide content with keys: job_responsibilities ,job_qualifications  ,job_preferred_skills ,job_company_culture,job_benefits, more_details. "}
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
                        
                        raw_description = response_data['candidates'][0]['content']['parts'][0]['text']
                        print("RAW DESCRIPTION:", raw_description[:200], "...")  # preview first 200 chars

                        # Step 2: Remove ```json markers if present
                        cleaned = re.sub(r"^```json\s*", "", raw_description)
                        cleaned = re.sub(r"\s*```$", "", cleaned)

                        # Step 3: Load the cleaned string as JSON
                        description_json = json.loads(cleaned)

                        # Step 4: Extract structured fields
                        job_responsibilities = description_json.get("job_responsibilities", [])
                        job_qualifications  = description_json.get("job_qualifications", [])
                        job_preferred_skills = description_json.get("job_preferred_skills", [])
                        job_company_culture  = description_json.get("job_company_culture", "")
                        job_benefits         = description_json.get("job_benefits", [])
                        more_details         = description_json.get("more_details", "")
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
                    job_responsibilities = job_responsibilities,
                    job_qualifications  = job_qualifications,
                    job_preferred_skills  = job_preferred_skills,
                    job_company_culture = job_company_culture,
                    job_benefits = job_benefits,
                    more_details = more_details
                    
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

        errors = []

        # Check required fields
        if not all([name, phone_number, official_email, address, industry, number_of_employees, password]):
            errors.append("All fields marked with * are required.")

        # Phone validation
        if not phone_number.isdigit():
            errors.append("Phone number must contain only digits.")
        elif len(phone_number) < 10:
            errors.append("Phone number must be at least 10 digits.")

        # Email validation
        if Company.objects.filter(official_email=official_email).exists():
            errors.append("Email is already registered.")
        if "@gmail.com" in official_email:
            errors.append("Gmail addresses are not allowed for company email.")

        # Password rules validation
        if len(password) < 8 or len(password) > 40:
            errors.append("Password must be 8–40 characters long.")
        if not re.search(r"[a-z]", password):
            errors.append("Password must include at least one lowercase letter.")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must include at least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            errors.append("Password must include at least one number.")
        if not re.search(r"[!@#$%^&*_\-?.]", password):
            errors.append("Password must include at least one special character (!@#$%^&*_-?.).")

        # If errors, show messages and stop
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('company_register')

        # If everything is valid, create Company and User
        hashed_password = make_password(password)
        company = Company.objects.create(
            name=name,
            phone_number=phone_number,
            official_email=official_email,
            website=website,
            address=address,
            industry=industry,
            number_of_employees=number_of_employees,
            password=hashed_password,
        )

        if not User.objects.filter(email=official_email + "+company").exists():
            user = User.objects.create_user(
                username=official_email + "+company",
                email=official_email,
                password=password,
            )
            company_group, created = Group.objects.get_or_create(name="Company")
            user.groups.add(company_group)
            user.save()

        messages.success(request, "Company registration successful!")
        return redirect('company_register')

    return render(request, 'company_register.html')

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
        
    return render(request,'company_login1.html')


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

import json

# def parse_field(field_text):
#     """
#     Convert a stringified list to a Python list.
#     If it's already a proper JSON list, parse it.
#     Otherwise, wrap it in a single-element list.
#     """
#     if not field_text:
#         return []
    
#     field_text = field_text.strip()
    
#     # If it looks like a list but uses single quotes, fix it
#     if field_text.startswith("[") and field_text.endswith("]"):
#         try:
#             # replace single quotes with double quotes for JSON parsing
#             fixed_text = field_text.replace("'", '"')
#             return json.loads(fixed_text)
#         except json.JSONDecodeError:
#             # fallback: split by comma for safety
#             items = [item.strip() for item in field_text[1:-1].split(",")]
#             return items
    
#     # Otherwise, wrap as single-element list
#     return [field_text]


import json
import re

def parse_field(field_text):
    """
    Convert a string or list-like string into a Python list of items.
    - If it's a JSON list (starts with [), parse it.
    - If it's a Python-like list (single quotes), convert and parse.
    - If it's a plain string, wrap in a single-element list.
    """
    if not field_text:
        return []

    field_text = field_text.strip()

    # Case 1: Proper JSON list
    if field_text.startswith("[") and field_text.endswith("]"):
        try:
            return json.loads(field_text)
        except json.JSONDecodeError:
            # Case 2: Python-like list with single quotes
            try:
                fixed_text = field_text.replace("'", '"')
                return json.loads(fixed_text)
            except json.JSONDecodeError:
                # fallback: split by comma but keep items as paragraphs
                items = [item.strip() for item in re.split(r",\s*(?=[A-Z])", field_text[1:-1])]
                return items

    # Case 3: Already a Python list object (rare, if passed directly)
    if isinstance(field_text, list):
        return field_text

    # Case 4: Plain string (single paragraph or multiple sentences)
    return [field_text]


def card_detail(request, id):
    job = Job.objects.filter(pk=id).first()
    if not job:
        return render(request, "404.html", {"message": "Job not found."})

    job_data = {}
    job_data = {
        "job_title": job.job_title,
            "job_type": job.job_type,
            "experience": job.job_experience,
            "location": job.job_location,
            "salary_range": job.job_salary,
            "job_responsibilities": parse_field(job.job_responsibilities),
            "job_qualifications": parse_field(job.job_qualifications),
            "job_preferred_skills": parse_field(job.job_preferred_skills),
            "job_company_culture": parse_field(job.job_company_culture),
            "job_benefits": parse_field(job.job_benefits),
            "more_details": parse_field(job.more_details),
        }
    print("JOB DATA:", job_data)

    return render(request, "job_detail.html", {
        "job": job,
        "job_data": job_data
    })



# Assuming your user model is linked to a Company model
@login_required
def all_job_applications(request):
    try:
        print("job")
        company = Company.objects.get(official_email = request.user.email)
        print(company)
        company_jobs = Job.objects.filter(company=company)
        all_applications = JobApplication.objects.filter(job__in=company_jobs).order_by('-applied_at')

        
        context = {
            'company': company,
            'applications': all_applications,
        }
        return render(request, 'applications_dashboard.html', context)
    except Company.DoesNotExist:
        # Handle the case where the user is not a company, e.g., redirect to an error page
        return render(request, 'company_app/not_a_company.html')

# Assuming your user model is linked to a Company model
@login_required
def job_applications(request,id):
    try:
        print("job")
        company = Company.objects.get(official_email = request.user.email)
        print(company)
        job = get_object_or_404(Job, pk=id)
        print(job)
        all_applications = JobApplication.objects.filter(job=job).order_by('-applied_at')

        
        context = {
            'company': company,
            'job':job,
            'applications': all_applications,
        }
        return render(request, 'job_applications.html', context)
    except Company.DoesNotExist:
        # Handle the case where the user is not a company, e.g., redirect to an error page
        return render(request, 'company_app/not_a_company.html')

   
@login_required
def update_job_status(request, job_id):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
        data = json.loads(request.body)
        new_status = data.get('status')
        print(new_status)
        job = Job.objects.get(id=job_id)
        job.job_status = new_status
        job.save()
        
        return JsonResponse({'success': True})
    except Job.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Job not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)