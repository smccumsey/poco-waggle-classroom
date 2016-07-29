from django.contrib import admin
from .models import Course, Module, Assessment, Content, Related, FlowModel, CredentialsModel

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(Content)
admin.site.register(Related)
admin.site.register(FlowModel)
admin.site.register(CredentialsModel)
