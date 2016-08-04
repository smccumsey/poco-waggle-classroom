from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return "Course: %s" % self.name

class Module(models.Model):
    name = models.CharField(max_length = 128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return "Course: %s, Module: %s" % (self.course, self.name)

class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.TextField()
    soln = models.FileField(upload_to="/home/smccumsey/waggle-classroom//waggle/solnFiles/", default="challenge1soln_DCR6J7d.py")
    def __str__(self):
        return "Module: %s, Assessment: %s" % (self.module, self.id)

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    ipython_notebooks = models.FilePathField(path='/waggle/assesment/content/notebooks/')
    videos = models.FilePathField(path='/waggle/assessment/content/videos/')
    def __str__(self):
        return "Module ( %s ) Content" % self.module

class Related(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    links = models.TextField()
    def __str__(self):
        return "Related from %s" % self.module

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course_progress = models.ManyToManyField(Course, through='CourseProgress', through_fields=('student','course'))
    module_progress = models.ManyToManyField(Module, through='ModuleProgress', through_fields=('student','module'))
    assessment_progress = models.ManyToManyField(Assessment, through='AssessmentProgress', through_fields=('student','assessment'))
    content_progress = models.ManyToManyField(Content, through='ContentProgress', through_fields=('student','content'))
    def __str__(self):
        return "Student with email: %s" % self.user.email

class CourseProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date_enrolled = models.DateTimeField()
    def __str__(self):
        return "Student: %s progress for Course: %s" % (self.student, self.course)

class ModuleProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return "Student: %s progress for Module: %s" % (self.student, self.module)

class AssessmentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True)
    code_submission = models.TextField()
    submission_feedback = models.TextField()
    def __str__(self):
        return "Student: %s progress for Assessment: %s" % (self.student, self.assessment)

class ContentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)
    video_notes = models.TextField()
    video_timepoint = models.DecimalField(max_digits=5, decimal_places=2)
    notebook_download_count = models.PositiveSmallIntegerField()
    def __str__(self):
        return "Student: %s progress for Content: %s" % (self.student, self.content)

    

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
