import uuid
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.forms import ValidationError
from seeker_app.models import Seeker

# Validator for official email
def validate_official_email(value):
    # TODO:later active
    # if not value.endswith(('.com', '.org', '.net', '.edu', '.gov', '.in')):
    #     raise ValidationError("Please provide a valid official email address.")
    # if value.endswith("@gmail.com"):
    #     raise ValidationError("Gmail addresses are not allowed for the company email.")
    pass
    
class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Retail', 'Retail'),
    ]

    EMPLOYEE_CHOICES = [
        ('1-10', '1-10 Employees'),
        ('11-50', '11-50 Employees'),
        ('51-200', '51-200 Employees'),
        ('201-500', '201-500 Employees'),
        ('501+', '501+ Employees'),
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        blank=True,
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    )
    official_email = models.EmailField(
        unique=True,
        null=False,
        validators=[validate_official_email]
    )
    website = models.URLField(blank=True,)
    address = models.TextField()
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    number_of_employees = models.CharField(max_length=20, choices=EMPLOYEE_CHOICES)
    password = models.CharField(max_length=255)  # Consider hashing this before saving
    gst_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', "Enter a valid GST number.")]
    )
    is_verified=models.BooleanField(default=False,null=True)
    pan_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', "Enter a valid PAN number.")]
    )
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    
    # form_filler_designation = models.CharField(max_length=100)
    # form_filler_name = models.CharField(max_length=255)
    # form_filler_email = models.EmailField(
    #     validators=[EmailValidator(message="Enter a valid email address.")]
    # )
    # form_filler_phonenumber = models.CharField(
    #     max_length=15,
    #     validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    # )

    def __str__(self):
        return f"{self.name} - {self.official_email}"

class Job(models.Model):
    Workplace_type=[
        ('On-site','On-site'),
        ('Hybrid','Hybrid'),
        ('Remote','Remote'),
    ]
    job_type_choices = [
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Contract', 'Contract'),
    ('Temporary', 'Temporary'),
    ('Other', 'Other'),
    ('Volunteer', 'Volunteer'),
    ('Internship', 'Internship'),
    ]

    jobpost_name = models.CharField(max_length=255)
    jobpost_phoneno = models.CharField(max_length=255)
    jobpost_email = models.CharField(max_length=255)
    jobpost_designation = models.CharField(max_length=255)
    
    job_title = models.CharField(max_length=255)
    job_workplace = models.CharField(max_length=255 , choices=Workplace_type)
    job_location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255 , choices=job_type_choices)
    job_no_opening = models.CharField(max_length=255)
    job_salary  = models.CharField(max_length=255)
    job_experience = models.CharField(max_length=25, blank=True)
    job_skills=models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    unique_number = models.CharField(default="0",max_length=255,null=True)
    # unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True)

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    seeker = models.ForeignKey(
        Seeker, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('interview', 'Interview Scheduled')
        ],
        default='pending'
    )
    resume = models.FileField(
        upload_to='job_application_resumes/',
        null=True,
        blank=True
    )
    cover_letter = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Application {self.job.job_title} : {self.seeker.full_name}"


    class Meta:
        unique_together = ('seeker', 'job')
        
        
class JobQuestion(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Question for {self.job.job_title}: {self.question_text}"

class ApplicationAnswer(models.Model):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        JobQuestion,
        on_delete=models.CASCADE
    )
    answer_text = models.TextField()

    class Meta:
        unique_together = ('application', 'question')