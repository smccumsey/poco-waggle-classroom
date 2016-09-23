from django.contrib import admin
from .models import Course, Module, Assessment, Content, Related, Video, AssessmentSubmission
from .models import Student, CourseProgress, ModuleProgress, AssessmentProgress, VideoProgress, ContentProgress

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(Content)
admin.site.register(Video)
admin.site.register(Related)
admin.site.register(Student)
admin.site.register(CourseProgress)
admin.site.register(ModuleProgress)
admin.site.register(ContentProgress)
admin.site.register(AssessmentProgress)
admin.site.register(VideoProgress)
admin.site.register(AssessmentSubmission)