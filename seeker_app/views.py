from django.shortcuts import *
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .models import *
from mywebsite.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
from company_app.models import Job
from django.http import HttpResponse
from django.http import JsonResponse
import datetime
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def seeker_jobs(request):
    job = Job.objects.all()
    print(job)
    return render(request, 'seeker_jobs.html',{"job":job})



@csrf_protect
def seeker_register(request):
    
    if request.method == "POST":
        full_name = request.POST.get("name")
        print(full_name)
        email_id = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        mobile_number = request.POST.get("mobile")
        work_status = request.POST.get("work_status")
        promotions = request.POST.get("promotions", "off") == "on"

        # Validation
        errors = []
        if not full_name or not email_id or not password or not confirm_password or not mobile_number or not work_status:
            errors.append("All fields marked with * are required.")
        if password != confirm_password:
            errors.append("Password and Confirm Password do not match.")
        if Seeker.objects.filter(email_id=email_id).exists():
            errors.append("Email is already registered.")

        if errors:
            return render(request, "seeker_register.html", {"errors": errors, 
                                                            "full_name": full_name, 
                                                            "email_id": email_id,
                                                            "mobile_number": mobile_number,
                                                            "work_status": work_status,
                                                            "promotions": promotions})

        # Save data to Seeker_Register (without password and confirm_password)
        seeker = Seeker.objects.create(
            full_name=full_name,
            email_id=email_id,
            mobile_number=mobile_number,
            work_status=work_status,
            promotions=promotions,
        )
        SeekerLanguage.objects.create(seeker=seeker)
        SeekerEducation.objects.create(seeker=seeker)
        SeekerInternship.objects.create(seeker=seeker)
        SeekerProject.objects.create(seeker=seeker)
        SeekerCompetitiveExam.objects.create(seeker=seeker)
        SeekerProfileEmployment.objects.create(seeker=seeker)
        SeekerAcademicAchievement.objects.create(seeker=seeker)
 
        # Create User instance for authentication
        user = User.objects.create_user(
            username=email_id+"+seeker",  # Using email as username
            email=email_id,
            password=password  # The password will be hashed automatically
        )
        user.first_name = full_name  # Optional: Set the user's first name
        user.save()
        
        try:
            employee_group = Group.objects.get(name="Employee")  # Get the group
            user.groups.add(employee_group)  # Assign the user to the group
        except Group.DoesNotExist:
            errors.append("The 'Employee' group does not exist. Please contact admin.")
            employee_group = Group.objects.create(name="Employee")  # Create the group if it doesn't exist
            user.groups.add(employee_group)  # Assign the user to the group
        return redirect(request, "seeker_register.html", {
            "errors": errors,
            "full_name": full_name,
            "email_id": email_id,
            "mobile_number": mobile_number,
            "work_status": work_status,
            "promotions": promotions
        })
  
            
     
        return redirect('success')  # Redirect to a success page
    return render(request, "seeker_register.html")


def seeker_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email+"+seeker", password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  # Redirect to the desired page after login
        else:
            # Display error message if credentials are incorrect
            messages.error(request, "Invalid email or password.")
            return redirect('seeker_login')  # Stay on the login page

    return render(request, 'seeker_login.html')

def seeker_forgot_password(request):
    context= {"step": "1"}
    
    if request.method == "POST":
        step=request.POST.get('step', '1')
        print("Step:", step)
        email = request.POST.get('email')
        if step == "2":
            if not Seeker.objects.filter(email_id=email).exists():
                context = {'step': "1"}
                messages.error(request, "Email not found.")
            else:
                messages.success(request, "OTP has been sent to your email.")
                context = {'step': "2", 'email': email}
        if step == "3":
            action=request.POST.get('action')
            if action == "resend_otp":
                if not Seeker.objects.filter(email_id=email).exists():
                    messages.error(request, "Email not found.")
                # Logic to resend OTP goes here
                messages.success(request, "OTP has been resent to your email.")
                context = {'step': "2", 'email': email}
            else:
                otp = request.POST.get('otp')
                if not otp:
                    messages.error(request, "OTP is required.")
                    context = {'step': "2", 'email': email}
                if not Seeker.objects.filter(email_id=email).exists():
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
            elif not Seeker.objects.filter(email_id=email).exists():
                messages.error(request, "Email not found.")
                context = {'step': "2", 'email': email}
            else:
                try:
                    user = User.objects.get(username=email+"+seeker")
                    user.set_password(password)  # Hash the new password
                    user.save()
                    messages.success(request, "Password changed successfully. You can now login.")
                    return redirect('seeker_login')  # Redirect to login page
                except Seeker.DoesNotExist:
                    messages.error(request, "Seeker not found.")
                    context = {'step': "1"}

    return render(request, 'seeker_forgot_password.html',context)


def _handle_multi_entry_section(request, seeker, config):

    model = config['model']
    post_fields = config['post_fields']
    model_fields = config['model_fields']
    required_fields_check = config.get('required_fields', [model_fields[0]])
    type_conversions = config.get('type_conversions', {})

    data_lists = [request.POST.getlist(field) for field in post_fields]

    model.objects.filter(seeker=seeker).delete()

    for values in zip(*data_lists):
        row_data = dict(zip(model_fields, values))
        if not any(row_data.get(field) for field in required_fields_check):
            continue
        for field_name, conversion_type in type_conversions.items():
            value = row_data.get(field_name)
            if value:
                if conversion_type == 'date':
                    row_data[field_name] = datetime.datetime.strptime(value, "%Y-%m-%d")
                elif conversion_type == 'float':
                    row_data[field_name] = float(value)
                elif conversion_type == 'int':
                    row_data[field_name]= int(value)
            else:
                row_data[field_name] = None
        
        model.objects.create(seeker=seeker, **row_data)

EDUCATION_CONFIG = {
            'model': SeekerEducation,
            'post_fields': ["degree[]", "institution[]", "year_of_starting[]", "year_of_passing[]", "marks[]"],
            'model_fields': ['degree', 'institution', 'year_of_starting', 'year_of_passing', 'marks'],
            'required_fields': ['degree', 'institution'],
            'type_conversions': {
                'year_of_starting': 'date',
                'year_of_passing': 'date',
                'marks': 'float'
            }
        }
        
LANGUAGE_CONFIG = {
            'model': SeekerLanguage,
            'post_fields': ["language_name[]", "proficiency[]"],
            'model_fields': ['language_name', 'proficiency'],
        }
INTERNSHIP_CONFIG = {
           'model': SeekerInternship,
            'post_fields': ['company_name[]', "role[]", 'duration[]'],
            'model_fields': ['company_name', 'role', 'duration'],
            'required_fields': ['company_name', 'duration'],
}

ACADEMIC_CONFIG ={
     'model': SeekerAcademicAchievement,
            'post_fields': ['achievement[]'],
            'model_fields': ['achievement'],
            'required_fields': ['achievement'],
}
        
PROJECT_CONFIG = {
            'model': SeekerProject,
            'post_fields': ["project_title[]", "project_description[]"],
            'model_fields': ['project_title', 'project_description'],
        }

EXAM_CONFIG = {
            'model': SeekerCompetitiveExam,
            'post_fields': ["exam_name[]", "competitive_score[]"],
            'model_fields': ['exam_name', 'competitive_score'],
            'type_conversions': {'competitive_score': 'float'}
        }

EMPLOYMENT_CONFIG = {
            'model': SeekerProfileEmployment,
            'post_fields': ['employment_company_name[]', "employment_role[]", 'employment_start_date[]', "employment_end_date[]"],
            'model_fields': ['employment_company_name', 'employment_role', 'employment_start_date', 'employment_end_date'],
            'required_fields': ['employment_company_name', 'employment_role'],
            'type_conversions': {
                'employment_start_date': 'date',
                'employment_end_date': 'date'
            }
        }

        
def seeker_profile(request):
    seeker = Seeker.objects.get(email_id = request.user.email)
    
    
    if request.method =="POST":     
        try:
            with transaction.atomic():
                _handle_multi_entry_section(request, seeker, EDUCATION_CONFIG)
                _handle_multi_entry_section(request, seeker, LANGUAGE_CONFIG)
                _handle_multi_entry_section(request, seeker, PROJECT_CONFIG)
                _handle_multi_entry_section(request, seeker, INTERNSHIP_CONFIG)
                _handle_multi_entry_section(request, seeker, ACADEMIC_CONFIG)
                _handle_multi_entry_section(request, seeker, EXAM_CONFIG)
                _handle_multi_entry_section(request, seeker, EMPLOYMENT_CONFIG)
            
            messages.success(request, "Profile updated successfully!")
            return redirect('seeker_profile')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            
        return redirect('/seeker_app/seeker_profile')
        
    context = {
        'seeker': seeker,
        'educations': SeekerEducation.objects.filter(seeker=seeker),
        'languages': SeekerLanguage.objects.filter(seeker=seeker),
        'internships': SeekerInternship.objects.filter(seeker=seeker),
        'projects': SeekerProject.objects.filter(seeker=seeker),
        'exams': SeekerCompetitiveExam.objects.filter(seeker=seeker),
        'employments': SeekerProfileEmployment.objects.filter(seeker=seeker),
        'achievements': SeekerAcademicAchievement.objects.filter(seeker=seeker),
    }
    return render(request,"seeker_profile.html", context)

DELETABLE_MODELS = {
    'education': SeekerEducation,
    'language': SeekerLanguage,
    'project': SeekerProject,
    'exam': SeekerCompetitiveExam,
    'employment': SeekerProfileEmployment,
    'internship':SeekerInternship,
    "achievement":SeekerAcademicAchievement
    # Add any other models you want to make deletable here
}


@login_required
@require_POST
def delete_field(request, field, pk):
    # 1. Look up the model class from our secure map
    model_class = DELETABLE_MODELS.get(field)

    # 2. If the field name is not in our map, it's an invalid request.
    if not model_class:
        return JsonResponse({'status': 'error', 'message': 'Invalid field type.'}, status=400)

    # 3. Get the seeker profile linked to the logged-in user

    try:
        # 4. Securely get the object, ensuring it belongs to the current seeker
        obj = model_class.objects.get(pk=pk)
        
        # 5. Delete the object and return success
        obj.delete()
        return JsonResponse({'status': 'ok', 'message': 'Entry deleted successfully.'})
    
    except model_class.DoesNotExist:
        # 6. If the object doesn't exist or doesn't belong to the user, return a 404 error.
        return JsonResponse({'status': 'error', 'message': 'Object not found.'}, status=404)
    except Exception as e:
        # Catch any other potential errors
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)