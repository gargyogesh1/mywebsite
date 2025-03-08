from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# from .models import Seeker_Register,SeekerProfile
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('home')
    


def home(request):
    print(request.user)
    return render(request, 'home.html')

# @api_view(['GET', 'POST'])
def common(request):
    # return Response(status = status.HTTP_200_OK)
    return render(request, 'common.html')

def success(request):
    # return Response(status = status.HTTP_200_OK)
    return render(request, 'success.html')


# @csrf_protect
# def seeker_register(request):
#     if request.method == "POST":
#         full_name = request.POST.get("name")
#         email_id = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")
#         mobile_number = request.POST.get("mobile")
#         work_status = request.POST.get("work_status")
#         promotions = request.POST.get("promotions", "off") == "on"

#         # Validation
#         errors = []
#         if not full_name or not email_id or not password or not confirm_password or not mobile_number or not work_status:
#             errors.append("All fields marked with * are required.")
#         if password != confirm_password:
#             errors.append("Password and Confirm Password do not match.")
#         if Seeker_Register.objects.filter(email_id=email_id).exists():
#             errors.append("Email is already registered.")

#         if errors:
#             return render(request, "seeker_register.html", {"errors": errors, 
#                                                             "full_name": full_name, 
#                                                             "email_id": email_id,
#                                                             "mobile_number": mobile_number,
#                                                             "work_status": work_status,
#                                                             "promotions": promotions})

#         # Save data to Seeker_Register (without password and confirm_password)
#         seeker = Seeker_Register.objects.create(
#             full_name=full_name,
#             email_id=email_id,
#             mobile_number=mobile_number,
#             work_status=work_status,
#             promotions=promotions,
#         )

#         # Create User instance for authentication
#         user = User.objects.create_user(
#             username=email_id,  # Using email as username
#             email=email_id,
#             password=password  # The password will be hashed automatically
#         )
#         user.first_name = full_name  # Optional: Set the user's first name
#         user.save()
        
#         try:
#             employee_group = Group.objects.get(name="Employee")  # Get the group
#             user.groups.add(employee_group)  # Assign the user to the group
#         except Group.DoesNotExist:
#             errors.append("The 'Employee' group does not exist. Please contact admin.")
#             return render(request, "seeker_register.html", {
#                 "errors": errors,
#                 "full_name": full_name,
#                 "email_id": email_id,
#                 "mobile_number": mobile_number,
#                 "work_status": work_status,
#                 "promotions": promotions
#             })
            
#         return redirect('success')  # Redirect to a success page

#     return render(request, "seeker_register.html")

# def company_login(request):
#     if request.method == "POST":
#         email=request.POST.get('email')
#         password = request.POST.get('password')
        
#         if "@gmail.com" in email:
#             messages.error(request,"Its not be a official email id")
#             return redirect('company_login')
#         else:
#             emailid = email
        
        
#         user1 = authenticate(request,username= emailid , password = password)
        
#         if user1 is not None:
#             login(request,user1)
#             return redirect('home')
#         else:
#             messages.error(request,"Invalid email id or password")
#             return redirect('company_login')
        
#     return render(request,'company_login.html')
        
# def seeker_login(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Authenticate the user
#         user = authenticate(request, username=email, password=password)
        
#         if user is not None:
#             # Login the user
#             login(request, user)
#             return redirect('home')  # Redirect to the desired page after login
#         else:
#             # Display error message if credentials are incorrect
#             messages.error(request, "Invalid email or password.")
#             return redirect('seeker_login')  # Stay on the login page

#     return render(request, 'seeker_login.html')


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        # Check if the email exists
        if User.objects.filter(email=email).exists():
            # Generate password reset link and send email
            user = User.objects.get(email=email)
            print(user)
            reset_token = default_token_generator.make_token(user)
            
            # Create your reset URL and send it via email
            reset_link = f"http://127.0.0.1:8000/reset-password/{user.pk}/{reset_token}/"

            # reset_url = request.build_absolute_uri(f"/reset_password/{reset_token}/")
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('forgot_password')
        else:
            messages.error(request, "No user is registered with this email address.")
            return redirect('forgot_password')
    
    return render(request, 'forgot_password.html')

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

def reset_password(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)

        # Validate the token
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('reset_password', user_id=user_id, token=token)

                # Set the new password and save the user
                user.set_password(new_password)
                user.save()

                messages.success(request, "Your password has been reset successfully.")
                return redirect('seeker_login')  # Redirect to login page after reset

            return render(request, 'reset_password.html', {'user_id': user_id, 'token': token})

        else:
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('seeker_login')  # Redirect to login if token is invalid

    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('seeker_login')  # Redirect to login if user does not exist

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Company_Register
# from django.contrib.auth.hashers import make_password  # For hashing the password


# def company_register(request):
    
#     if request.method == "POST":
#         name = request.POST.get('name')
#         phone_number = request.POST.get('phone_number')
#         official_email = request.POST.get('official_email')
#         website = request.POST.get('website')
#         address = request.POST.get('address')
#         industry = request.POST.get('industry')
#         number_of_employees = request.POST.get('number_of_employees')
#         password = request.POST.get('password')
        
#         errors = []
#         if not name or not phone_number or not official_email or not website or not address or not industry or not number_of_employees or not password:
#             errors.append("All Fields marked with * are required. ")
#         if not phone_number.isdigit():
#             errors.append("Phone number must contain only digits.")
#         if len(phone_number)<10:
#             errors.append("Phone number must be at least 10 digits.")
#         if Company_Register.objects.filter(official_email=official_email).exists():
#             errors.append("Email is already registered.")
#         if "@gmail.com" in official_email:
#             errors.append("Gmail addresses are not allowed for the company email.")
#         if len(password) < 8:
#             errors.append("Password must be at least 8 characters long.")  
        
#         if errors:
#             for error in errors:
#                 messages.error(request, error)
#         else:
#             hashed_password = make_password(password)
 
#             company = Company_Register.objects.create(
#                 name = name,
#                 phone_number=phone_number,
#                 official_email=official_email,
#                 website=website,
#                 address=address,
#                 industry=industry,
#                 number_of_employees=number_of_employees,
#                 password=hashed_password,
#             )
#             if not User.objects.filter(email=official_email).exists():
#                 # Add the user to the User table
#                 user = User.objects.create_user(
#                     username=official_email,  # Use email as the username
#                     email=official_email,
#                     password=password,
#                 )
                
#             try:
#                 company_group = Group.objects.get(name="Company")  # Fetch the "Company" group
#                 user.groups.add(company_group)  # Add the user to the group
#             except Group.DoesNotExist:
#                  print("The 'Company' group does not exist. Please create it in the Admin panel.")
            

#             messages.success(request, "User added to the system.")
#             messages.success(request,"Company registration Sucessfully!")
#         return redirect('company_register')
#     return render(request,'company_register.html')

from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.files.storage import FileSystemStorage

def seeker_profile(request):
    print(request.user.email)
    
    seeker=Seeker_Register.objects.get(email_id=request.user.email)
    profile=SeekerProfile()
    
    if seeker.profile :
        profile=seeker.profile
        preferences=SeekerProfilePreference.objects.filter(seekerProfile=profile)
        for pref in preferences:
            print(pref.name)
    else:
        profile.save()
        seeker.profile=profile
        seeker.save()
    if request.method == "POST":
        try:
            print("post")
            # Retrieve and validate the email (as primary key)
            # Retrieve basic profile preference
            preference_name = request.POST.get("job_type", "")
            print(preference_name)
            preference = SeekerProfilePreference.objects.create(seekerProfile=profile,name=preference_name)
            # Retrieve education details
            print(preference)
            preference.save()
            degree = request.POST.get("degree", "").strip()
            institution = request.POST.get("institution", "").strip()
            year_of_passing = request.POST.get("year", "").strip()

            if not degree or not institution or not year_of_passing:
                messages.error(request, "Please fill out all education fields.")
                return redirect("seeker_profile")

            education, created = SeekerProfileEducation.objects.get_or_create(
                degree=degree, institution=institution, year_of_passing=year_of_passing
            )
            print(education)  # Check if the education object is being created correctly


            print(education)
            # Save resume
            resume_file = request.FILES.get("resume")
            if resume_file:
                fs = FileSystemStorage()
                resume_instance = SeekerProfileResume.objects.create(file=resume_file)
            else:
                resume_instance = None

            # Create profile summary
            summary_text = request.POST.get("summary", "").strip()
            summary_instance, _ = SeekerProfileSummary.objects.get_or_create(summary=summary_text)

            # Update profile with the new fields
            profile.preference = preference
            profile.education = education
            profile.resume = resume_instance
            profile.profile_summary = summary_instance

            # Save key skills (ManyToMany)
            skills = request.POST.get("skills", "").split(",")
            for skill in skills:
                skill = skill.strip()
                if skill:
                    key_skill, _ = SeekerProfileKeySkill.objects.get_or_create(skill_name=skill)
                    profile.key_skills=key_skill

            # Save languages (ManyToMany)
            languages = request.POST.get("language", "").split(",")
            proficiencies = request.POST.get("proficiency", "").split(",")
            for lang, prof in zip(languages, proficiencies):
                if lang and prof:
                    language_instance, _ = SeekerProfileLanguage.objects.get_or_create(
                        name=lang.strip(),
                        proficiency=prof.strip()
                    )
                    profile.languages=(language_instance)

            # Save internships (ManyToMany)
            company_name = request.POST.get("company_name", "").strip()
            role = request.POST.get("role", "").strip()
            duration = request.POST.get("duration", "").strip()
            if company_name and role and duration:
                internship, _ = SeekerProfileInternship.objects.get_or_create(
                    company_name=company_name, role=role, duration=duration
                )
                profile.internships=(internship)

            # Save projects (ManyToMany)
            project_title = request.POST.get("project_title", "").strip()
            project_description = request.POST.get("project_description", "").strip()
            if project_title and project_description:
                project, _ = SeekerProfileProject.objects.get_or_create(
                    title=project_title, description=project_description
                )
                profile.projects=(project)

            # Save accomplishments (ManyToMany)
            accomplishments = request.POST.get("accomplishments", "").split(",")
            for acc in accomplishments:
                if acc.strip():
                    accomplishment, _ = SeekerProfileAccomplishment.objects.get_or_create(title=acc.strip())
                    profile.accomplishments=(accomplishment)

            # Save competitive exams (ManyToMany)
            exam_name = request.POST.get("exam_name", "").strip()
            exam_score = request.POST.get("exam_score", "").strip()
            if exam_name and exam_score:
                exam, _ = SeekerProfileCompetitiveExam.objects.get_or_create(
                    exam_name=exam_name, score=exam_score
                )
                profile.competitive_exams=(exam)

            # Save employment details (ManyToMany)
            company_name = request.POST.get("company_name", "").strip()
            role = request.POST.get("role", "").strip()
            duration = request.POST.get("duration", "").strip()
            if company_name and role and duration:
                employment, _ = SeekerProfileEmployment.objects.get_or_create(
                    company_name=company_name, role=role, duration=duration
                )
                profile.employment=(employment)

            # Save academic achievements (ManyToMany)
            academic_achievements = request.POST.get("academic_achievements", "").split(",")
            for achievement in academic_achievements:
                if achievement.strip():
                    academic, _ = SeekerProfileAcademicAchievement.objects.get_or_create(achievement=achievement.strip())
                    profile.academic_achievements=(academic)

            # Save the profile
            profile.save()
            seeker.profile=profile
            seeker.save()
            # Final success message
            messages.success(request, "Profile created or updated successfully!")
            return redirect("seeker_profile")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, "seeker_profile.html")

    context={
        "profile":profile
    }
    return render(request, "seeker_profile.html",context=context)
