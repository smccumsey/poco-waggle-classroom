from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return self.title

def assessment_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_<id>/module_<id>/assessmentFiles/<filename>
    return 'course_{0}/module_{1}/assessmentFiles/{2}'.format(instance.module.course.id, instance.module.id, filename)

class Assessment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessments')
    description = models.TextField()
    assess_file = models.FileField(upload_to=assessment_directory_path, null=True)
    code_editor_filler = models.TextField(null=True)
    order = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return 'assessment_%s from %s' % (self.order, self.module.title)

def notebook_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_<id>/module_<id>/notebooks/<filename>
    return 'course_{0}/module_{1}/notebooks/{2}'.format(instance.module.course.id, instance.module.id, filename)

def video_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_<id>/module_<id>/videos/<filename>
    return 'course_{0}/module_{1}/videos/{2}'.format(instance.module.course.id, instance.module.id, filename)

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    title = models.TextField(null=True)
    html_notebook = models.FileField(upload_to=notebook_directory_path, null=True)
    def __str__(self):
        return '%s (content for %s)' % (self.title, self.module.title)

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.TextField(null=True)
    video_URL = models.URLField(null=True);
    def __str__(self):
        return '%s (video for %s)' % (self.title, self.module.title)

class Related(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='relateds')
    title = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    link = models.URLField(null=True,blank=True);
    notebook = models.FileField(upload_to=notebook_directory_path, null=True, blank=True)
    def __str__(self):
        return 'related_%s from %s' % (self.id, self.module.title)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students')
    course_progress = models.ManyToManyField(Course, through='CourseProgress', through_fields=('student','course'))
    module_progress = models.ManyToManyField(Module, through='ModuleProgress', through_fields=('student','module'))
    assessment_progress = models.ManyToManyField(Assessment, through='AssessmentProgress', through_fields=('student','assessment'))
    video_progress = models.ManyToManyField(Video, through='VideoProgress', through_fields=('student','video'))
    def __str__(self):
        return "Student with email: %s" % self.user.email

class CourseProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False)
    date_enrolled = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return "%s progress for %s course" % (self.student, self.course)

class ModuleProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    started = models.BooleanField(default=False)
    def __str__(self):
        return "%s progress for %s module" % (self.student, self.module)

class AssessmentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True)
    code_submission = models.TextField(default="#Type python code below")
    errors_list = models.TextField(default='')
    def __str__(self):
        return "%s progress for %s" % (self.student, self.assessment)

class VideoProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    video_notes = models.TextField(null=True)
    video_timepoint = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    def __str__(self):
        return "%s progress for %s" % (self.student, self.video)

    

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
