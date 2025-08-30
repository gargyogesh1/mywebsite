from django.db import models
from django.core.exceptions import ValidationError

 
class Seeker(models.Model):
    WORK_STATUS_CHOICES = [
        ('experienced', 'Experienced'),
        ('fresher', 'Fresher'),
    ]
    
    full_name = models.CharField(max_length=200)
    email_id = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES)
    promotions = models.BooleanField(default=False)
    
    seekerPreference = models.CharField(max_length=255,null=True,blank=True)
    skills = models.ManyToManyField('Skill', related_name='seekers', blank=True)
    profile_summary = models.TextField(max_length = 555 ,null=True,blank=True)
    resume = models.FileField(null=True,blank=True)
    def clean(self):
        """
        Add custom validation logic here.
        """
        if len(self.mobile_number) < 10 or not self.mobile_number.isdigit():
            raise ValidationError("Mobile number must be at least 10 digits and numeric.")
        if self.work_status not in dict(self.WORK_STATUS_CHOICES):
            raise ValidationError("Work status must be either 'Experienced' or 'Fresher'.")
    
    def __str__(self):
        return self.full_name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class SeekerEducation(models.Model):
    Education = [
        ('TENTH', '10th'),
        ('TWELFTH', '12th'),
        ('DIPLOMA', 'Diploma'),
        ('GRADUATION', 'Graduation'),
        ('POSTGRADUATION', 'Postgraduation'),
        ('HIGHER_STUDIES', 'Higher Studies'),
    ]
    
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    degree = models.CharField(max_length=255 , choices=Education)
    institution = models.CharField(max_length=255,null=True)
    year_of_starting = models.DateField(null=True, blank=True)
    year_of_passing = models.DateField(null=True, blank=True)
    marks = models.FloatField(null=True)
    def __str__(self):
        return f"{self.degree} from {self.institution} of {self.seeker.email_id}"

  
class SeekerLanguage(models.Model):
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    language_name = models.CharField(max_length=255 ,null=True )
    proficiency = models.CharField(max_length=255 , choices=[
        ('basic','Basic'),
        ('istermediate','Intermedicate',),
        ('advanced','Advanced'),
    ])
    def __str__(self):
        return f"{self.language_name} ({self.proficiency})"

class SeekerInternship(models.Model):
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.role} at {self.company_name}"


class SeekerProject(models.Model):
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    project_description = models.TextField(null=True, blank=True)
    def __str__(self):
        return  f"{self.id} {self.project_title}"
    

class SeekerCompetitiveExam(models.Model):
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    # competitive_score = models.CharField(max_length=50)
    competitive_score = models.FloatField(null=True)


    def __str__(self):
        return f"{self.exam_name} - {self.competitive_score}"


class SeekerProfileEmployment(models.Model):
    seeker = models.ForeignKey('Seeker',on_delete=models.CASCADE)
    employment_company_name = models.CharField(max_length=255,null=True)
    employment_role = models.CharField(max_length=255,null=True)
    employment_start_date = models.DateField(null=True, blank=True)
    employment_end_date = models.DateField(null=True, blank=True)  # Allow ongoing jobs

    def __str__(self):
        return f"{self.employment_role} at {self.employment_company_name}"


class SeekerAcademicAchievement(models.Model):
    seeker = models.ForeignKey("Seeker",on_delete=models.CASCADE)
    achievement = models.TextField(null=True)

    def __str__(self):
        return self.achievement[:50]  # Display first 50 characters

