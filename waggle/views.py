from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView, CreateView
from waggle.forms import CodeForm
from django.contrib.auth.models import User
from .models import Related, Content, Assessment, Module, Course, AssessmentProgress, Video, VideoProgress, Student

from django.utils import timezone
from datetime import datetime
import subprocess
import re
import json
import imp
import ntpath
from importlib.machinery import SourceFileLoader
import os
import sys
import subprocess
from shutil import copyfile
from django.template import RequestContext
from oauth2client import client, crypt
from django.conf import settings
from django.contrib.auth.decorators import login_required

import os
import logging
import httplib2
from django.contrib.auth import login, authenticate
from django.template.defaultfilters import slugify

class LessonView(generic.DetailView):
    from django.template.defaultfilters import slugify
    template_name = 'waggle/lesson.html'
    model = User

    """
    Constructor. Called in the URLconf; can contain helpful extra
    keyword arguments, and other things.
    """
    #module_id = self.kwargs.get('module')
    #assessments = Assessment.objects.filter(module_id=module_id)
    #contents = Content.objects.filter(module_id=module_id)
    #relateds = Related.objects.filter(module_id=module_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LessonView, self).get_context_data(**kwargs)
        module_id = self.kwargs.get('module')
        print('MODULE_ID ', module_id)
        context['module_obj'] = Module.objects.get(id=module_id)
        context['assessments'] =Assessment.objects.filter(module_id=module_id)
        context['contents'] =Content.objects.filter(module_id=module_id)
        context['videos'] =Video.objects.filter(module_id=module_id)
        context['relateds'] =Related.objects.filter(module_id=module_id)
        print(context.items())
        # set up progress data for student if it doesnt exist
        student_instance = context['object'].students
        for assessment_instance in context['assessments']:
            assessment_prog,created = student_instance.assessmentprogress_set.get_or_create(assessment=assessment_instance)
            print(assessment_prog,created)
            print(assessment_prog.errors_list)
        for video_instance in context['videos']:
            video_prog,created = student_instance.videoprogress_set.get_or_create(video=video_instance)
            print(video_prog,created)
        return context

    def setupEnv(self, code, envFile):
        test_filename = '/home/smccumsey/waggle-classroom/waggle/media/tmp/test.py'
        code_lines = code.splitlines()
        new_code = '\n\t#user submission'.expandtabs(4)+'\n'+'\n'.join(map(lambda s:('\t'+s).expandtabs(4),code_lines)) #lines after first must be indented
        print(new_code)
        with open(test_filename, "w") as outfile, open(envFile, 'r', encoding='utf-8') as infile:
            text = infile.read()
            text_with_code = re.sub('&&&', new_code, text,flags=re.M)
            text_with_code = re.sub('# paste user code here', '', text_with_code,flags=re.M)
            outfile.write(text_with_code)
        return test_filename

    def runCode(self, fname):
        try:
            p = subprocess.Popen('python '+fname, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            return p.communicate()  # this gets you pipe values
        except Exception as e:
            return 'error'+e
        else:
            return "else"

    def post(self, request, *args, **kwargs):
        postdata = request.POST.dict()
        print('POST DATA')
        print(postdata)
        if(request.POST.get('html_notes')):
            updated_note_table = request.POST.get('html_notes')
            videoID = request.POST.get('videoID')
            video_timepoint = request.POST.get('time')

            video_progress = VideoProgress.objects.get(student=Student.objects.get(user=request.user), video=Video.objects.get(id=int(videoID)))
            video_progress.video_notes = updated_note_table
            video_progress.video_timepoint= video_timepoint
            video_progress.save()
            return HttpResponse('django says the note was saved')
        if(request.POST.get('submittedcode')):
            usr_code = request.POST.get('submittedcode')
            assessmentID = request.POST.get('assessmentID')
            print('USRCODE: %s \nassessID: %s' % (usr_code, assessmentID))
            envFile = Assessment.objects.get(id=int(assessmentID)).assess_file.path
            testFile = self.setupEnv(usr_code, envFile)
            result_feedback = list(map(lambda x: x.decode('ASCII'), self.runCode(testFile)))
            print('RAW RESULT',result_feedback)
            if result_feedback[0]:
                parsed_result_feedback  = json.dumps([ {k:str(v) for k,v in (eval(err)).items()} for err in result_feedback[0].splitlines()])
            elif result_feedback[1]:
                parsed_result_feedback = "bad"
            else:
                parsed_result_feedback = "good"
            print('PARSED RESULT',parsed_result_feedback)
            assessment_progress = AssessmentProgress.objects.get(student=Student.objects.get(user=request.user), assessment=Assessment.objects.get(id=int(assessmentID)))
            assessment_progress.code_submission = usr_code
            assessment_progress.errors_list = parsed_result_feedback
            assessment_progress.save()
            return HttpResponse(parsed_result_feedback)
        return self.get(request, *args, **kwargs)

class MenuView(generic.DetailView):
    template_name = 'waggle/menu.html'
    model=User

    # student_instance = user_instance.students
    # module_prog = ModuleProgress.create(student=student_instance)
    def get(self, request, *args, **kwargs):
        request.session['course_title'] = self.kwargs['course']
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuView, self).get_context_data(**kwargs)
        courses = [(slugify(c.title),c) for c in Course.objects.all()]
        course_title= self.kwargs.get('course')
        course_lookup = [c[1] for c in courses if c[0]==course_title].pop() #sloppy
        context['modules'] = Module.objects.filter(course_id=course_lookup.id)
        return context

class ProfileView(generic.DetailView):
    template_name = 'waggle/profile.html'
    model = User

    # student_instance = user_instance.students
    # course_prog = CourseProgress.create(student=student_instance)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class GoogleView(generic.TemplateView):
    template_name = 'waggle/google8a43fbed4f8a62b6.html'

class LoginView(generic.TemplateView):
    template_name = 'waggle/login.html'

    def post(self, request, *args, **kwargs):
        usr_token = request.POST.get('idtoken')
        user = authenticate(token=usr_token)
        print("USERID!",user,user.pk)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('foo')
                return HttpResponse(json.dumps({'pk':user.pk}))

                # Redirect to a success page.
            else:
                print('bar')
                # Return a 'disabled account' error message
        else:
            print('baz')
            # Return an 'invalid login' error message.

