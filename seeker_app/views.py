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

def example_view(request):
    return HttpResponse("This is a placeholder view.")


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
        seeker.save()
        # Create User instance for authentication
        user = User.objects.create_user(
            username=email_id,  # Using email as username
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
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  # Redirect to the desired page after login
        else:
            # Display error message if credentials are incorrect
            messages.error(request, "Invalid email or password.")
            return redirect('seeker_login')  # Stay on the login page

    return render(request, 'seeker_login.html')

def seeker_profile(request):
    seeker = Seeker.objects.get(email_id = request.user.email)

    if request.method =="POST":
        degree = request.POST.get("degree")
        institution = request.POST.get("institution")
        year_of_starting = request.POST.get("year_of_starting")
        year_of_passing = request.POST.get("year_of_passing")
        marks = request.POST.get("marks")
        
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
        
        if year_of_passing == "":
            year_of_passing=None
        if year_of_starting == "":
            year_of_starting=None
        if marks=="":
            marks=None
        if competitive_score=="":
            competitive_score=None
        
        education  = SeekerEducation.objects.create(
            degree = degree,
            institution = institution,
            year_of_starting = year_of_starting,
            year_of_passing = year_of_passing,
            marks = marks,
            seeker= seeker,
        )
        education.save()   
        
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
            competitive_score = competitive_score,
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
    return render(request,"seeker_profile.html")

