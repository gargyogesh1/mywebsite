from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Company)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(JobQuestion)
admin.site.register(ApplicationAnswer)
