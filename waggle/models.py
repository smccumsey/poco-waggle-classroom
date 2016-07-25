from django.db import models


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
    soln = models.FileField(upload_to="/Users/smeo/django_waggle/mysite/waggle/solnFiles/", default="challengeXsoln.py")
    tests = models.TextField()
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
'''
class UserStats(models.Model):
pass
'''
