from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(studentsReg)
admin.site.register(courseSchedules)
admin.site.register(Instructor)