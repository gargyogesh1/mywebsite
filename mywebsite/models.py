from django.db import models
from django.core.exceptions import ValidationError
# from seeker_app.models import SeekerProfile


from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

# def validate_official_email(value):
#     if value.endswith("@gmail.com"):
#         raise ValidationError("Gmail addresses are not allowed for the company email.")


# class SeekerProfileEducation(models.Model):
#     seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
#     degree = models.CharField(max_length=255)
#     institution = models.CharField(max_length=255)
#     year_of_passing = models.IntegerField()
#     def __str__(self):
#         return f"{self.degree} from {self.institution}"

# class SeekerProfileKeySkill(models.Model):
#     skill_name = models.CharField(max_length=255)
#     def __str__(self):
#        return self.skill_name
   
# class SeekerProfileLanguage(models.Model):
    
#     name = models.CharField(max_length=255)
#     proficiency = models.CharField(max_length=255 , choices=[
#         ('basic','Basic'),
#         ('istermediate','Intermedicate',),
#         ('advanced','Advanced'),
#     ])
#     def __str__(self):
#         return f"{self.name} ({self.proficiency})"

# class SeekerProfileInternship(models.Model):
#     company_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
#     duration = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.role} at {self.company_name}"


# class SeekerProfileProject(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     def __str__(self):
#         return self.title
# class SeekerProfileSummary(models.Model):
#     summary = models.TextField()

#     def __str__(self):
#         return self.summary[:50]  # Display first 50 characters


# class SeekerProfileAccomplishment(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.title


# class SeekerProfileCompetitiveExam(models.Model):
#     exam_name = models.CharField(max_length=255)
#     score = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.exam_name} - {self.score}"
    
# class SeekerProfileEmployment(models.Model):
#     company_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)  # Allow ongoing jobs

#     def __str__(self):
#         return f"{self.role} at {self.company_name}"


# class SeekerProfileAcademicAchievement(models.Model):
#     achievement = models.TextField()

#     def __str__(self):
#         return self.achievement[:50]  # Display first 50 characters


# class SeekerProfileResume(models.Model):
#     file = models.FileField(upload_to='resumes/')

#     def __str__(self):
#         return f"Resume {self.id}"
    
    
    
# class SeekerProfile(models.Model):
#    # Add email as primary key    


#     def __str__(self):
#         return f"Seeker Profile "
    
    
# # class Seeker(models.Model):
# #     WORK_STATUS_CHOICES = [
# #         ('experienced', 'Experienced'),
# #         ('fresher', 'Fresher'),
# #     ]

# #     full_name = models.CharField(max_length=200)
# #     email_id = models.EmailField(unique=True)
# #     mobile_number = models.CharField(max_length=15)
# #     work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES)
# #     promotions = models.BooleanField(default=False)
# #     profile_summary = models.ForeignKey(SeekerProfileSummary,null=True , on_delete=models.CASCADE, related_name="profile")
# #     resume = models.OneToOneField(SeekerProfileResume,null=True , on_delete=models.CASCADE, related_name="profile")
# #     seekerProfilePreference = models.CharField(max_length=255)

# #     def clean(self):
# #         """
# #         Add custom validation logic here.
# #         """
# #         if len(self.mobile_number) < 10 or not self.mobile_number.isdigit():
# #             raise ValidationError("Mobile number must be at least 10 digits and numeric.")
# #         if self.work_status not in dict(self.WORK_STATUS_CHOICES):
# #             raise ValidationError("Work status must be either 'Experienced' or 'Fresher'.")
    
# #     def __str__(self):
# #         return self.full_name
