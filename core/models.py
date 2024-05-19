from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Students(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    def __str__(self):
        return self.user.username
class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class courseSchedules(models.Model):
    id = models.IntegerField(primary_key=True)
    days = models.IntegerField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=10)
class Courses(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,null=True)
    capacity = models.IntegerField()
    scheduleid = models.ForeignKey(courseSchedules,on_delete=models.CASCADE,null=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_by')

class studentsReg(models.Model):
    id = models.IntegerField(primary_key=True)
    studentId = models.ForeignKey(Students,on_delete=models.CASCADE)
    courseId = models.ForeignKey(Courses,on_delete=models.CASCADE)
