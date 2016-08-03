from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length = 128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.TextField()
    soln = models.FileField(upload_to="/home/smccumsey/waggle-classroom//waggle/solnFiles/", default="challenge1soln_DCR6J7d.py")
    def __str__(self):
        return "Challenge %s from %s" % (self.id, self.module)

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    ipython_notebooks = models.FilePathField(path='/waggle/assesment/content/notebooks/')
    videos = models.FilePathField(path='/waggle/assessment/content/videos/')
    def __str__(self):
        return "Content from %s" % self.module

class Related(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    links = models.TextField()
    def __str__(self):
        return "Related from %s" % self.module

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField()
    '''
    registered_courses
    module_progress
    # assessment progress
    history_of_submitted_code
    submission_results
    # content progress
    video_notes
    video_time
    '''
