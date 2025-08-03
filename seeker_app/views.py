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


def seeker_profile(request):
    seeker = Seeker.objects.get(email_id = request.user.email)
    
    
    if request.method =="POST":
        degrees = request.POST.getlist("degree[]")
        institutions = request.POST.getlist("institution[]")
        starting_years = request.POST.getlist("year_of_starting[]")
        passing_years = request.POST.getlist("year_of_passing[]")
        marks_list = request.POST.getlist("marks[]")

        
        language_name = request.POST.get("language_name")
        proficiency = request.POST.get("proficiency")
        
        project_title = request.POST.get("project_title")
        project_description = request.POST.get("project_description")
        
        exam_name = request.POST.get('exam_name')
        competitive_score = request.POST.get("competitive_score")
        
        employment_company_name = request.POST.get('employment_company_name')
        employment_role = request.POST.get("employment_role")
        employment_start_date = request.POST.get('employment_start_date')
        employment_end_date = request.POST.get("employment_end_date")


                
        for i in range(len(degrees)):
            degree = degrees[i]
            institution = institutions[i]
            year_of_starting = starting_years[i] or None
            year_of_passing = passing_years[i] or None
            marks = marks_list[i] or None

            # Skip empty or incomplete entries
            if not degree and not institution:
                continue
            exists = SeekerEducation.objects.filter(
                degree=degree,
                institution=institution,
                seeker=seeker
            ).exists()
            if exists:
                continue  
            
            
            SeekerEducation.objects.create(
                degree=degree,
                institution=institution,
                year_of_starting=year_of_starting,
                year_of_passing=year_of_passing,
                marks=marks,
                seeker=seeker
            )

        
        language = SeekerLanguage.objects.create(
            language_name = language_name,
            proficiency = proficiency,
            seeker= seeker,
        )
        language.save()
        
        project = SeekerProject.objects.create(
            project_title = project_title,
            project_description = project_description,
            seeker= seeker,
        )
        project.save()
            
        competitive = SeekerCompetitiveExam.objects.create(
            exam_name = exam_name,
            competitive_score = float(competitive_score) if competitive_score!="" else 0,
            seeker = seeker,
        )
        competitive.save()
        
        employment = SeekerProfileEmployment.objects.create(
            employment_company_name = employment_company_name,
            employment_role = employment_role,
            employment_start_date = employment_start_date,
            employment_end_date = employment_end_date,
            seeker= seeker,
        )
        
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
    print( "Total ed1",SeekerEducation.objects.filter(seeker=seeker)[0].id) 
    return render(request,"seeker_profile.html", context)


def delete_education(request, edu_id):
    if request.method == 'POST':
        try:
            edu = SeekerEducation.objects.get(id=edu_id)
            print("Edu to delete",edu)
            edu.delete()
            return JsonResponse({'status': 'ok'})
        except SeekerEducation.DoesNotExist:
            return JsonResponse({'status': 'not found'})